import base64
import jwt
import requests

from .constant import INVALID_SESSION_ID, MALFORMED_TOKEN, SESSION_ID_MISSING
from .exception import InvalidSSORequest


class SSOConnectorClient:

    def __init__(self, client_id,
                 client_secret,
                 endpoint="https://api.ssoconnector.com"):
        self.__client_id = client_id
        self.__client_secret = client_secret
        self.__endpoint = endpoint

    def __decoded_response(self, response):
        try:
            return jwt.decode(response,
                              self.__client_secret,
                              algorithms=["HS256"])
        except Exception:
            raise InvalidSSORequest(MALFORMED_TOKEN)

    def __get_api_key(self):
        key = f"#{self.__client_id}@{self.__client_secret}"
        return base64.b64encode(key.encode("ascii")).decode("ascii")

    def __consume_session_id(self, session_id):
        body = {
            "token": session_id
        }
        headers = {
            "X-Api-Key": self.__get_api_key()
        }
        url = f"{self.__endpoint}/sso/session/consume"

        api_response = requests.post(url, body=body, headers=headers)

        if api_response.status_code != 200:
            raise InvalidSSORequest(INVALID_SESSION_ID)

    def sso_response(self, response):
        decoded_response = self.__decoded_response(response)

        session_id_key = "session_id"

        if session_id_key not in decoded_response:
            raise InvalidSSORequest(SESSION_ID_MISSING)

        self.__consume_session_id(decoded_response[session_id_key])

        return decoded_response
