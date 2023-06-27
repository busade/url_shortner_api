from ..utils import db
from datetime import datetime


class Links(db.Model):
    __tablename__ = 'links'
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(255), nullable=False, unique=True)
    long_url = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow )
    qr_code = db.Column(db.LargeBinary, nullable=False)
    custom_url = db.Column(db.String, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    analytics = db.relationship('Analysis', backref='links', lazy=True)

    def __repr__(self):
        return f'<Links {self.id}>'
    
    def save(self):
        db.session.add(self)
        db.session.commit()


    def delete(self):
        db.session.delete(self)
        db.session.commit()
    @classmethod
    def get_by_id(self, id):
        return self.query.get_or_404(id)


class Analysis(db.Model):
    __tablename__ = 'analysis'
    id = db.Column(db.Integer, primary_key=True)
    link_id = db.Column(db.Integer, db.ForeignKey('links.id'))
    ip_address = db.Column(db.String, nullable=False)
    country = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)   
    date = db.Column(db.DateTime, default=datetime.utcnow)
    visit_count = db.Column(db.Integer, default=0)  


    def __repr__(self):
        return f'<Analysis {self.id},{self.visits_count}>'
    

    def save(self):
        db.session.add(self)
        db.session.commit() 

    def delete(self):
        db.session.delete(self)
        db.session.commit()