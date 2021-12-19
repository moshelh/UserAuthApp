from fastapi import APIRouter, Depends, HTTPException
import database
from datetime import timedelta
from schema import User, Token, UserInDB, UserLogIn
from sqlalchemy.orm import Session
from repository import users
from starlette import status

router = APIRouter()

ACCESS_TOKEN_EXPIRE_MINUTES = 30


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: UserLogIn, db: Session = Depends(database.get_db)):
    user = users.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = users.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me")
async def read_users_me(current_user: User = Depends(users.get_current_active_user)):
    return current_user


@router.post("/user/signIn", response_model=User)
async def sign_in(request: UserInDB, db: Session = Depends(database.get_db)):
    return users.create(request, db)
