from flask_sqlalchemy import SQLAlchemy
import datetime
import json as j
import re
from flask import Flask


db = SQLAlchemy()

if __name__ == "__main__":
    #Creates table
    import pymysql
    pymysql.install_as_MySQLdb()
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI']='mysql://localhost/ysport'
    db = SQLAlchemy(app)



def setup_db(_db):
    global db
    db=_db

def add_to_db(obj):
    db.session.add(obj)
#    db.session.flush()
    db.session.commit()
    return obj

def save():
  db.session.commit()
  
def remove_from_db(obj):
    db.session.delete(obj)
    db.session.commit()



class User(db.Model):
    """ Table to hold User information """

    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    nick = db.Column(db.String(25), unique=True)
    password = db.Column(db.String(100))
    text = db.Column(db.String(200))

    def __init__(self, params):
        valid_nick = re.compile(r'^[a-zA-Z0-9_.-]*$') #only allows letters, numbers and _ . -
        if valid_nick.search(params['nick']):
          self.nick = params['nick']
          self.email = params['email']
          self.password = params['password'] #hash somewhere here
          self.text = params['text']
    
    @staticmethod
    def create(params, json=False):
        data = add_to_db(User(params))

        if json:
            data = to_dict(data)

        return data

    @staticmethod
    def auth(nick, password):
        user = db.sssion.query(User).filter_by(nick=nick).first()
        return user.password == password

    def change_nick(self, new_nick):
        self.nick = new_nick
        save()



class Video(db.Model):
    __tablename__ = 'video'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(100))
    text = db.Column(db.String(250))
    views = db.Column(db.Integer, default=0)

    #--- REMOVE THIS----#
    upvotes = db.Column(db.Integer, default=0)
    downvotes = db.Column(db.Integer, default=0)
    #-------------------#

    upload_date = db.Column(db.DateTime)
    
    def __init__(self, params):
        self.user_id = params['user_id']
        self.text = params['text']
        self.title = params['title']
        self.upload_date = datetime.datetime.utcnow()

    def json(self):
        tmp = {o.name: getattr(self, o.name) for o in self.__table__.columns} 
        data = {key: tmp[key] for key in tmp if any(cls in str(type(tmp[key])) for cls in['int', 'str', 'float'])}
        return j.dumps(data)
    
    @staticmethod
    def find_by_id(id):
      return db.session.query(Video).filter_by(id=id).first()
    
    @staticmethod
    def create(params):
        return add_to_db(Video(params))


    @staticmethod
    def get_accumulative_vote(id):
        return db.session.query(Vote).filter(id=id).count()

    @staticmethod
    def get_hot(id, page, per=10):
        pass
        #db.session.query(Vote).filter(
        #return db.session.query(Video).order_by(Video.upvotes)#.paginate(page=page, per_page=per)

    def set_view(self, view_count):
        self.views += view_count
        save()

    @staticmethod
    def get_featured(id, page, per=10):
        return db.session.query(Video).order_by(Video.views).paginate(page=page, per_page=per)

    @staticmethod
    def get_new(id, page, per=10):
      return db.session.query(Video).order_by(Video.upload_date).paginate(page=page, per_page=per)



class Vote(db.Model):
    __tablename__ = "vote"
    id = db.Column(db.Integer, primary_key=True)
    way = db.Column(db.Integer, default=-1)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'))
    date = db.Column(db.DateTime, nullable=False)
    parent_type = db.Column(db.String(20), nullable=False)

    def __init__(self, params):
        self.user_id = params['user_id']
        self.date = datetime.datetime.utcnow()
        self.parent_type = params['parent_type']

        if params['parent_type'] == 'video':
            self.video_id = params['video_id']

        elif params['parent_type'] == 'comment_id':
            self.comment_id = params['comment_id']

        try:
            self.way = params['way']

        except:
            self.way = -1

    @staticmethod
    def create(params):
        return add_to_db(Vote(params))


    def set_way(self, way):
        self.way = way
        save()


    @staticmethod
    def create(params):
        return add_to_db(Vote(params))


    @staticmethod
    def find_by_video_id(video_id, user_id=None):
        if user_id is None:
            return db.session.query(Vote).filter_by(video_id=video_id).all()
        return db.session.query(Vote).filter_by(video_id=video_id, user_id=user_id).all()

    @staticmethod
    def find_by_time(hours, minutes=0, parent_types=['video', 'comment']):
        print 'INCLUDING MINUTE IN SEARCH FOR DEV'
        return db.session.query(Vote).filter(Vote.parent_type.in_(
            parent_types), Vote.date < datetime.datetime.utcnow()
            +datetime.timedelta(hours=hours, minutes=minutes)).all()



class Thread(db.Model):
  __tablename__ = "thread"
  id = db.Column(db.Integer, primary_key=True)
  video_id = db.Column(db.Integer, db.ForeignKey('video.id'))
  

  def __init__(self, params):
    self.video_id = params['video_id'] or None
  

  @staticmethod
  def create(params):
    return add_to_db(Thread(params))
  

  @staticmethod
  def find_by_video_id(video_id):
    return db.session.query(Thread).filter_by(video_id=video_id)



class Comment(db.Model):
  __tablename__ = "comment"
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  thead_id = db.Column(db.Integer, db.ForeignKey('thread.id'))
  text = db.Column(db.String(250),nullable =False)
  time = db.Column(db.DateTime)
  
  @staticmethod
  def find_by_thread_id(thread_id):
    return db.session.query(Comment).filter_by(thread_id=thread_id)


class Mention(db.Model):
  __tablename__ = "mention"
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  mentioned_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
  
  @staticmethod
  def find_by_comment_id(comment_id):
    return db.session.query(Mention).filter_by(comment_id=comment_id)

   
  
class Tag(db.Model):
    __tablename__ = "tag"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'))
if __name__ == "__main__":
    db.create_all()
    db.session.commit()
