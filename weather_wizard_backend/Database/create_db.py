# Built-in Imports
from datetime import datetime
from io import BytesIO

# Flask
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'dev'
db = SQLAlchemy(app)

# Picture table. By default, the table name is filecontent
class FileContent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    data = db.Column(db.LargeBinary, nullable=False)  # Actual data, needed for Download
    text = db.Column(db.Text)
    pic_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'Pic Name: {self.name}, created on: {self.pic_date}'

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        filename = file.filename
        file_stream = file.read()
        newFile = FileContent(name=filename, data=file_stream)
        db.session.add(newFile)
        db.session.commit()
        return 'File has been uploaded'

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
