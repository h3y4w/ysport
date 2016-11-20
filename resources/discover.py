from flask_restful import Resource, request
from flask_sqlalchemy import SQLAlchemy
import DB


class Discover (Resource):
    def get(self):
        sid = request.args.get('sid') or 0
        page = request.args.get('page') or 0
        section = request.args.get('section') or 'All'
        
        votes = DB.Vote.find_by_time(0, minutes=1)
        for vote in votes:
            
            if vote.parent_type == "video":
                print vote.video_id

            elif vote.parent_type == "comment":
                print vote.comment_id

        
class HotSection (Resource):

    def get(self):
        pass


class FeaturedSection (Resource):
    pass


class NewSection (Resource):
    pass

