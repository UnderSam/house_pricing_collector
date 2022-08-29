from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import dotenv_values
from pymongo import MongoClient
from .routes.house_record import router as RecordRouter
from fastapi_pagination import add_pagination

config = dotenv_values(".env")
app = FastAPI(
    title='591 House record collector',
    description='This is a project to collect and search records of 591 data',
    version='0.0.1',
)
origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(config['MONGO_CONNECT_URL'])
    app.database = app.mongodb_client[config['HOUSE_DB']]
    app.collection = app.database[config['HOUSE_COLLECTION']]

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()

app.include_router(RecordRouter)

@app.get('/')
async def root():
    return {'message': 'Hello world!'}

add_pagination(app)