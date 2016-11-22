from flask_restful import Resource, request
import DB
from response import ResponseAPI

class User (Resource):
    def post(self):
        error = False 
        message = "" 
        data = {}
         
        try:
            params = request.get_json(force=True)
            user = DB.User.create(params)
            if user is not None:
                data = {'id': user.id}
        except Exception as e:
            error = True
            message = str(e)

        finally:
            return ResponseAPI('User', 'post', error=error, message=message, data=data).json()
