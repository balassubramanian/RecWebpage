from typing_extensions import Annotated, Doc
from jose import jwt 
from typing import Any, Dict, Optional
from datetime import datetime, timedelta


from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.config import SECRET_KEY, ALGORITHM
class JwtRepo:

    def __init__(self,data:dict={}, token:str=None) -> None:
        self.data = data
        self.token = token

    def generate_token(self, expires_delta: Optional[timedelta]=None):
        to_encode =  self.data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes = 15)
        
        to_encode.update({"exp: expire"})
        encode_jwt = jwt.encode(to_encode, SECRET_KEY,algorithm = [ALGORITHM])

        return encode_jwt
    
    def decode_token(self):
        try: 
            decode_token = jwt.decode(self.token, SECRET_KEY, algorithm=[ALGORITHM])
            return decode_token if decode_token["expires"] >= datetime.time() else None
        except:
            return {}
    
    def extrect_token(token: str):
        return jwt.decode(token, SECRET_KEY, algorithm=[ALGORITHM])

class JWTBearer(HTTPException):
    def __init__(self, auto_error:bool = True):
        super(JWTBearer,self).__init__(auto_error=auto_error)

    async def __Call__(self,request:Request):
        credentials : HTTPAuthorizationCredentials = await super(JWTBearer, self)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail= {"status":"Forbidden", "message": " Invalid authentication Schema."})
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail= {"status":"Forbidden", "message": " Invalid TOKEN OR EXPIRED TOKEN."})
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail= {"status":"Forbidden", "message": " Invalid authorization code"})



