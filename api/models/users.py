from ..utils import db
from datetime import datetime



class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow )
    is_active = db.Column(db.Boolean, default=False)
    link = db.relationship('Links', backref='users', lazy=True)




    def __repr__(self):
        return f'<Users {self.id}>'
    

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
