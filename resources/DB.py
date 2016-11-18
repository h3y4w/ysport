from flask_sqlalchemy import SQLAlchemy
import datetime
import json as j

#FOR TESTING TO CREATE DB!
db = SQLAlchemy()

def setup_db(_db):
    global db
    db=_db

def add_to_db(obj):
    db.session.add(obj)
    db.session.flush()
    db.session.commit()
    return obj

def remove_from_db(obj):
    db.session.delete(obj)
    db.session.commit()

def to_dict(obj, json=False):
    temp = {o.name: getattr(obj, o.name) for o in obj.__table__.columns}
    if json:
        temp = j.dumps(temp)
    return temp

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    nick = db.Column(db.String(25))
    password = db.Column(db.String(100))
    text = db.Column(db.String(200))

    def __init__(self, params):
        self.nick = params['nick']
        self.password = params['password'] #hash somewhere here
        self.text = params['text']

    @staticmethod
    def create(params):
        return add_to_db(User(params))

    @staticmethod
    def auth(nick, password):
        user = db.sssion.query(User).filter_by(nick=nick).first()
        return user.password == password

class Video(db.Model):
    __tablename__ ='video'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String('100'))
    text = db.Column(db.String(250))
    views = db.Column(db.Integer, default=0)
    upvotes = db.Column(db.Integer, default=0)
    downvotes = db.Column(db.Integer, default=0)
    upload_date = db.Column(db.DateTime)
    
    def __init__(self, params):
        self.user_id = params['user_id']
        self.text = params['text']
        self.title = params['title']
        self.upload_date = datetime.datetime.utcnow()

    @staticmethod
    def create(params):
        return add_to_db(Video(params))

    @staticmethod
    def get_hot(id, page, per=10):
        return db.session.query(Video).order_by(Video.upvotes).paginate(page=page, per_page=per)

    @staticmethod
    def get_featured(id, page, per=10):
        return db.session.query(Video).order_by(Video.views).paginate(page=page, per_page=per)

    @staticmethod
    def get_new(id, page):
        pass

class Tag(db.Model):
    __tablename__ = "tag"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'))

if __name__ == "__main__":
    from flask import Flask
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI']='mysql://localhost/ysport'
    db = SQLAlchemy(app)
    db.create_all()
    db.session.commit()



