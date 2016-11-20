from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
import pymysql

pymysql.install_as_MySQLdb()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql://localhost/ysport'
api = Api(app)
db = SQLAlchemy(app)

from resources.discover import Discover
from resources.videos import Video, Videos
from resources.users import User
from resources.misc import Vote
#from resources.comments import Comments


if __name__ == "__main__":
    api.add_resource(Discover, '/discover')

    api.add_resource(User, '/user')

    api.add_resource(Video, '/video')
    api.add_resource(Videos, '/video/<int:id>')
    api.add_resource(Vote, '/video/<int:obj_id>/<string:way>')

    app.run()

