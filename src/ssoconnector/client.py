

import jwt
from .exception import InvalidRequest

class SSOConnectorClient:

  def __init__(self, client_id, client_secret):
    self.__client_id = client_id
    self.__client_secret = client_secret

  def sso_response(self, response):
    try:
      return jwt.decode(response, 
              self.__client_secret, 
              algorithms=["HS256"])
    except:
      raise InvalidRequest("Invalid Token")
