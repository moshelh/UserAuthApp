from datetime import datetime, timedelta
from typing import Optional

from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from starlette import status
from sqlalchemy.orm import Session
from . import logger

import database, model, schema
from schema import User, UserInDB, TokenData

SECRET_KEY = "98dd25cd9b2c8f2a365e7748cf2b82f75c1cbcb2048c974b424b9bc0a55b4453"
ALGORITHM = "HS256"


def get_user(db, username: str):
    user = db.query(model.User).filter(model.User.username == username).first()
    if username:
        return UserInDB(username=user.username, password=user.password)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(database.get_db(), username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if not current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def create(request: schema.UserInDB, db: Session):
    new_user = model.User(full_name=request.full_name, username=request.username,
                          password=str(get_password_hash(request.password)),
                          email=request.email, disabled=request.disabled)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    logger.logger(f'New user name :{request.username}', __name__, "INFO")

    return new_user
