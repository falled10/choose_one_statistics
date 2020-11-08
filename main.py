from fastapi import FastAPI, status
from fastapi.encoders import jsonable_encoder
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from api.statistics.routes import router as statistics_router
from core.settings import CORS_ORIGINS
from core.database import close_mongo_connection, connect_to_mongo


app = FastAPI()

app.add_event_handler('startup', connect_to_mongo)
app.add_event_handler('shutdown', close_mongo_connection)
app.add_middleware(CORSMiddleware, allow_origins=CORS_ORIGINS, allow_credentials=True,
                   allow_methods=['*'], allow_headers=['*'])
app.include_router(statistics_router, prefix='/api/statistics', tags=['statistics'])


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder({i['loc'][-1]: i['msg'] for i in exc.errors()})
    )
