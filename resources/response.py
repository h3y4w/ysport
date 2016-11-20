import json
class ResponseAPI (object):
  def __init__(self, method, obj, data=None,message=None, error=False):
    self.method = method
    self.obj = obj
    self.error = error
    self.message = message
    self.data = data
    
  def json(self):
      return json.dumps(self.__dict__)

