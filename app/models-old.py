from app import db

class Post(db.Model):
    __tablename__ = 'example'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    body = db.Column(db.Text)
 	
    def __init__(self, title, body):
        self.title = title
        self.body = body