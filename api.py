from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql://localhost/ysport'
api = Api(app)
db = SQLAlchemy(app)

from resources.discover import Discover
from resources.videos import Videos
#from resources.users import Users
#from resources.comments import Comments


if __name__ == "__main__":
    api.add_resource(Discover, '/discover')

    api.add_resource(Videos, '/video')
    db.create_all()
    app.run()
