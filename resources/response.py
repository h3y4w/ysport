import json
from DB import db

class ResponseAPI (object):
  def __init__(self, method, obj, data={},message="", error=False):
    self.method = method
    self.obj = obj
    self.error = error
    self.message = message
    self.data = data
    if error == True:
        db.session.rollback()

  def json(self):
      return self.__dict__
