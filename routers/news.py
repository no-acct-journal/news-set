from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_config import get_db
from schemas.base import NewsItemBase
from service import news_cache as news

router = APIRouter(prefix="/api/news", tags=["news"])

@router.get("/categories")
async def get_categories(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    categories = await news.get_categories(db, skip, limit)
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
    news_items = [
        NewsItemBase.model_validate(item).model_dump(by_alias=True, mode="json")
        for item in new_list
    ]
    total = await news.get_news_count(db, category_id)
    has_more = (offset + len(news_items)) < total
    return{
        "code" : 200,
        "message": "success",
        "data":{
            "list" : news_items,
            "total" : total,
            "hasMore" : has_more
        }
    }

@router.get("/detail")
async def get_news_detail(news_id: int = Query(..., alias="id"), db: AsyncSession = Depends(get_db)):
    news_detail = await news.get_news_detail(db, news_id)
    if not news_detail:
        raise HTTPException(status_code=404, detail="news not found")

    updated_views = await news.increase_news_views(db, news_detail.id)
    if updated_views is None:
        raise HTTPException(status_code=404, detail="news not found")

    related_news = await news.get_related_news(db, news_detail.id, news_detail.category_id)

    return {
        "code" : 200,
        "message": "success",
        "data": {
            "id": news_detail.id,
            "title": news_detail.title,
            "content": news_detail.content,
            "image": news_detail.image,
            "author": news_detail.author,
            "publishTime": news_detail.publish_time,
            "categoryId": news_detail.category_id,
            "views": updated_views,
            "relatedNews": related_news
        }
    }
