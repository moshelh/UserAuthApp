from fastapi import FastAPI

import database
import model
from routers import users

model.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.include_router(users.router)
