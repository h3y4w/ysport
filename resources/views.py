from flask_restful import Resource, request
from response import ResponseAPI
import DB

class View(Resource):


    def post(self):
        data = {}
        message = ""
        error = False

        try:
            params = request.get_json(force=True)
            tmp = DB.View.find_model_by_video_and_user_id(params['video_id'], params['user_id'])
            if tmp is not None:
                tmp.set_count(params['count'])
                data = tmp.json()
            else:

                data = DB.View.create(params).json()

        except Exception as e:
            message = str(e)
            error = True
            DB.session.rollback()

        finally:
            return ResponseAPI('View', 'post', data=data, message=message, error=error).json()

    def get(self):
        pass



class Views(Resource):

    def get(self, id):
        data = {}
        message = ""
        error = False

        try:
            data = DB.View.find_model_by_id(id).json()

        except Exception as e:
            message = str(e)
            error = True
            DB.session.rollback()

        finally:
            return ResponseAPI('Views', 'get', data=data, message=message, error=error).json()
