from flask_restful import Resource, request
from response import ResponseAPI
import DB

class Tags(Resource):

    def get(self, id):
        data = {}
        error = False
        message = "" 
        
        try:
            data = DB.Tag.find_model_by_id(id).json()

        except Exception as e:
            DB.session.rollback()
            message = str(e)
            error = True

        finally:
            return ResponseAPI('Tags', 'get', data=data, message=message, errror=error).json()



class Tag(Resource):

    def post(self):
        data = {}
        error = False
        message = "" 

        try:
            params = request.get_json(force=True)
            data = DB.Tag.create(params).json()

        except Exception as e:
            DB.session.rollback()
            message = str(e)
            error = True

        finally:
            return ResponseAPI('Tag', 'post', data=data, message=message, error=error).json()



class TagAttribute(Resource):

    def get(self):
        data = {}
        error = False
        message = ""

        try:
            search_word = request.args.get('search')
            if search_word is None:
                data = DB.convert_model_list(DB.TagAttribute.all())

            else:
                data = DB.TagAttribute.find_model_by_search(search_word).json()

        except Exception as e:
            DB.session.rollback()
            message = str(e)
            error = True
        
        finally:
            return ResponseAPI('TagAttribute', 'get', data=data, message=message, error=error).json()
        
    def post(self):
        data = {}
        error = False
        message = "" 

        try:
            params = request.get_json(force=True)
            data = DB.TagAttribute.create(params).json()

        except Exception as e:
            DB.session.rollback()
            message = str(e)
            error = True

        finally:
            return ResponseAPI('TagAttribute', 'post', data=data, message=message, error=error).json()



class TagAttributes(Resource):

    def get(self, id):
        data = {}
        error = False
        message = "" 
        try:
            data = DB.TagAttribute.find_model_by_id(id).json()

        except Exception as e:
            DB.session.rollback()
            message = str(e)
            error = True

        finally:
            return ResponseAPI('TagAttributes', 'get', data=data, message=message, error=error).json()

    
    def delete(self, id):
        data = {}
        error = False
        message = ""

        try:
            tag = DB.TagAttribute.find_model_by_id(id)
            #data['Success']=tag.delete()
        
        except Exception as e:
            DB.session.rollback()
            message = str(e)
            error = True

        finally:
            ResponseAPI('TagAttributes', 'delete', data=data, message=message, error=error).json()


