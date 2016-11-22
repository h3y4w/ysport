from flask_restful import Resource, request
import DB
from response import ResponseAPI
import traceback

class Vote (Resource):
    def post(self, obj_id, way):
        data = {}
        error = False
        message = "" 

        print 'USER ID IS DEFINED IN POST METHOD FOR TESTING!!!'
        user_id = 1

        try:
            parent_type = request.args['parent_type']

            vote = None

            if parent_type == 'video':
                vote = DB.Vote.find_model_by_video_and_user_id(obj_id, user_id)

            elif parent_type == 'comment': 
                vote = DB.vote.find_by_comment_and_user_id(obj_id, user_id)

            vote = vote or DB.Vote.create({'parent_type': parent_type, parent_type+'_id':obj_id, 'user_id': user_id}) 
            if way == "up":
                vote.set_way(1) 

            elif way == "down":
                vote.set_way(0)

            elif way == "remove":
                vote.set_way(-1)

            data = vote.json()

        except Exception as e:
            traceback.print_exc()
            message = str(e)
            error = True

        finally:
            return ResponseAPI('post', 'Vote', data=data, message=message, error=error).json()

