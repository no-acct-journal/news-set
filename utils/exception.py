import traceback

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from starlette import status

from config.settings import settings


async def http_exception_handler(request: Request, exc: HTTPException):
    """
    Handle HTTPException errors.
    """
    # HTTPException is usually raised by business logic, so data stays empty.
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code": exc.status_code,
            "message": exc.detail,
            "data": None
        }
    )


async def integrity_error_handler(request: Request, exc: IntegrityError):
    """
    Handle database integrity constraint errors.
    """
    error_msg = str(exc.orig)

    # Map common constraint errors to user-facing messages.
    if "username_UNIQUE" in error_msg or "Duplicate entry" in error_msg:
        detail = "Username already exists"
    elif "FOREIGN KEY" in error_msg:
        detail = "Related data does not exist"
    else:
        detail = "Data constraint conflict. Please check your input"

    # Include detailed error data in development mode.
    error_data = None
    if settings.app_debug:
        error_data = {
            "error_type": "IntegrityError",
            "error_detail": error_msg,
            "path": str(request.url)
        }

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "code": 400,
            "message": detail,
            "data": error_data
        }
    )


async def sqlalchemy_error_handler(request: Request, exc: SQLAlchemyError):
    """
    Handle SQLAlchemy database errors.
    """
    # Include detailed error data in development mode.
    error_data = None
    if settings.app_debug:
        error_data = {
            "error_type": type(exc).__name__,
            "error_detail": str(exc),
            # Format the traceback for logging and debugging.
            "traceback": traceback.format_exc(),
            "path": str(request.url)
        }

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "code": 500,
            "message": "Database operation failed. Please try again later",
            "data": error_data
        }
    )


async def general_exception_handler(request: Request, exc: Exception):
    """
    Handle all uncaught exceptions.
    """
    # Include detailed error data in development mode.
    error_data = None
    if settings.app_debug:
        error_data = {
            "error_type": type(exc).__name__,
            "error_detail": str(exc),
            # Format the traceback for logging and debugging.
            "traceback": traceback.format_exc(),
            "path": str(request.url)
        }

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "code": 500,
            "message": "Internal server error",
            "data": error_data
        }
    )



