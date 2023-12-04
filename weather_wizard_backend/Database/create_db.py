from datetime import datetime
from flask import Flask, request, render_template, redirect
from flask import SQLAlchemy
import base64

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class FileContent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    data = db.Column(db.LargeBinary, nullable=False)
    avg_color = db.Column(db.String(16), nullable=False) #store color as hexadecimal in string form
    pic_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = file.filename
            file_stream = file.read()
            newFile = FileContent(name=filename, data=file_stream)
            db.session.add(newFile)
            db.session.commit()
            return redirect('/images')
    return render_template('upload.html')

@app.route('/images')
def show_images():
    images = FileContent.query.all()
    encoded_images = [{'name': img.name, 'data': base64.b64encode(img.data).decode('ascii')} for img in images]
    return render_template('result.html', images=encoded_images)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
