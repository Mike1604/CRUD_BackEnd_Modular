import os
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

SECRET_KEY = os.getenv("SECRET_KEY", "GLOTOOLRefreshSecret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 2880
REFRESH_TOKEN_EXPIRE_DAYS = 7 

#Hashing con bcrypt
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def encrypt_password(plain_password: str) -> str:
    return bcrypt_context.hash(plain_password)

def verify_password(input_password: str, stored_password: str) -> bool:
    return bcrypt_context.verify(input_password, stored_password)

def create_jwt(data: dict, expires_delta: timedelta = None, is_refresh: bool = False) -> str:
    payload = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    payload.update({"exp": expire}) 
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(user_id: str) -> str:
    return create_jwt({"userId": user_id}, expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS), is_refresh=True)

def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")  
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id 
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except JWTError as e:
        print(f"Error decoding JWT: {str(e)}")
        raise HTTPException(status_code=401, detail="Invalid token")
