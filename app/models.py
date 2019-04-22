from . import db   
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255),unique = True,index = True)
    pitch_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    pass_secure = db.Column(db.String(255))
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    pitches = db.relationship('Pitch', backref='user', lazy="dynamic")


    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)


    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)

    def __repr__(self):
        return f'User {self.username}'


class Pitch(db.Model):
    __tablename__ = 'pitches'

    id = db.Column(db.Integer,primary_key = True)
    title= db.Column(db.String(300), index=True)
    content = db.Column(db.String(300), index=True)
    category_id = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    comments = db.relationship('Comment', backref='pitch', lazy="dynamic")
    time = db.Column(db.DateTime, default=datetime.utcnow)

    def save_pitch(self, pitch):
        ''' Save the pitches '''
        db.session.add(pitch)
        db.session.commit()

    # display pitches
    @classmethod
    def get_pitches(id):
        pitches = Pitch.query.filter_by(category_id = id).all()
        return pitches

class Comment(db.Model):

    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    post_comment = db.Column(db.String(255), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    pitches = db.Column(db.Integer, db.ForeignKey('pitches.id'))
    time = db.Column(db.DateTime, default=datetime.utcnow)

    def save_comment(self):
        ''' Save the comments '''
        db.session.add(self)
        db.session.commit()


    # display comments

    @classmethod
    def get_comments(cls, id):
        comments = Comment.query.filter_by(pitch_id=id).all()
        return comments        
        
    def __repr__(self):
        return f'User {self.name}'        