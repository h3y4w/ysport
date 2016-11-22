from datetime import datetime, timedelta
from functools import wraps
import jwt
from flask_restful import request

secret = "something-super-secret"

def login_required(roles=[]):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            try:
                token = Token.valid(request.headers['Authorization'])
            except KeyError:
                abort(409)
            if token.user_role not in roles and roles != [] :
                abort(409)
            return f(*args, **kwargs)
        return wrapped
    return wrapper

class Token (object): 
    def __init__(self, payload):
        self.user_id = payload['uid']
        self.user_nick = payload['unick']
        self.user_role = payload['urole']
        self.iat = payload['iat']
        self.exp = payload['exp']
        
    @staticmethod
    def valid(t):
        data = None
        try:
            data = jwt.decode(t, secret)
            
        except Exception:
            pass
       
        finally:
            return data
        
    @staticmethod
    def get(t):
        data = None
        try:
            data = jwt.decode(t, secret)
            
        except Exception:
            pass
       
        finally:
            if data is not None:
                return Token(data)
    
    @staticmethod
    def generate(user):
        print "TOKEN IS SET NOT TO EXPIRE FOR A YEAR!!!"
        payload = {
            'uid': user.id,
            'unick' user.nick,
            'urole': user.role,
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(days=365)
        }
        return jwt.encode(payload, secret)
