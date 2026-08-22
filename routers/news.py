from fastapi import Query

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

@router.get("/list")
async def get_news_list(
        category_id: int = Query(..., alias = "categoryId"),
        page: int = 1,
        page_size: int = Query(10, le = 100, alias = "pageSize"),
        db: AsyncSession = Depends(get_db)
):
    offset = (page - 1) * page_size
    new_list = await news.get_news_list(db, category_id, offset, page_size)
    total = await news.get_news_count(db, category_id)
    has_more = (offset + len(new_list)) < total
    return{
        "code" : 200,
        "message": "success",
        "data":{
            "list" : new_list,
            "total" : total,
            "hasMore" : has_more
        }
    }