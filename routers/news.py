from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_config import get_db
from service import news

router = APIRouter(prefix="/api/news", tags=["news"])

@router.get("/categories")
async def get_categories(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    categories = await news.get_category(db, skip, limit)
    return {
        "code" : 200,
        "message": "success",
        "data": categories
    }