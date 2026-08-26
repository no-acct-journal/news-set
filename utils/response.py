from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


def success_response(message: str = "success", data=None):
    content = {
        "code": 200,
        "message": message,
        "data": data
    }

    # Convert FastAPI, Pydantic, and ORM values into a consistent response body.
    return JSONResponse(content=jsonable_encoder(content))
