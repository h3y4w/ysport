import DB
from flask_restful import Resource
from response import ResponseAPI

class Comment(Resouce):
    def post(self):
        data = {}
        message = ""
        error = False
        
        try:
            data = db.Comment.create(request.get_json(force=True)).json()
            
        except Exception as e:
            message = str(e)
            error = True
            
        finally:
            if error is True:
                DB.db.session.rollback()
            ResponseAPI('Comment', 'post', data=data, message=message, error=error).json()
            
  
class Comments(Resource):
    def get(self, id):
        data = {}
        message = ""
        error = False
    
    try:
        data = DB.Comment.find_model_by_id(id).json()
    
    except AttributeError:
        
        message = "Cannot not be set"
        error = True
        
    except Exception as e:
        message = str(e)
        error = True
     
    finally:
        if error is True:
            DB.db.session.rollback()
        ResponseAPI('Comments', 'get', data=data, message=message, error=error)