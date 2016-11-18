from flask_restful import Resource, request
from flask_sqlalchemy import SQLAlchemy
import DB

db = SQLAlchemy()
def discover_setup(db_):
    global db
    db=db_



class Discover (Resource):
    def get(self):
        sid = request.args.get('sid') or 0
        page = request.args.get('page') or 0
        videos = DB.Video.get_most_hot(sid=sid, page=page)
        print videos
        
class HotSection (Resource):

    def get(self):
        pass


class FeaturedSection (Resource):
    pass


class NewSection (Resource):
    pass

