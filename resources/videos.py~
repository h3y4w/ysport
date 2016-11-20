from flask_restful import Resource, request
import DB

class Videos(Resource):
    def post(self):
        params = request.get_json(force=True)
        params['user_id']=3
        video = DB.Video.create(params)
        return DB.to_dict(video, json=True)
        
