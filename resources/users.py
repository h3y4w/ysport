from flask_restful import Resource, request
import DB
from response import ResponseAPI

class User (Resource):
    def post(self):
        error = False 
        message = None
        data = None
        
        try:
            params = request.get_json(force=True)
            data = DB.User.create(params, json=True)

        except Exception as e:
            error = True
            message = str(e)
           
        finally:
            return ResponseAPI('User', 'post', error=error, message=message, data=data).json()
