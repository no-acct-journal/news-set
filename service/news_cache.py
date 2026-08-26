from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession

from cache.news_cache import get_cached_categories, set_cache_categories, get_cache_news_list, set_cache_news_list, \
    get_cached_news_detail, cache_news_detail, get_cached_related_news, cache_related_news
from models.news import Category, News
from schemas.base import NewsItemBase
from schemas.news import NewsDetailResponse, RelatedNewsResponse


async def get_categories(db: AsyncSession, skip: int = 0, limit: int = 100):
    # Try cache first.
    cached_categories = await get_cached_categories()
    if cached_categories is not None:
        return cached_categories

    stmt = select(Category).offset(skip).limit(limit)
    result = await db.execute(stmt)
    categories = result.scalars().all()  # ORM

    # Write through to cache.
    if categories:
        categories = jsonable_encoder(categories)
        await set_cache_categories(categories)

    return categories


async def get_news_list(db: AsyncSession, category_id: int, skip: int = 0, limit: int = 10):
    # Convert offset and limit back into page and size for the cache key.
    page = skip // limit + 1
    cached_list = await get_cache_news_list(category_id, page, limit)
    if cached_list is not None:
        return [News(**item) for item in cached_list]

    stmt = select(News).where(News.category_id == category_id).offset(skip).limit(limit)
    result = await db.execute(stmt)
    news_list = result.scalars().all()

    if news_list:
        # Store Python-style field names because cached data is used by the backend.
        news_data = [NewsItemBase.model_validate(item).model_dump(mode="json", by_alias=False) for item in news_list]
        await set_cache_news_list(category_id, page, limit, news_data)

    return news_list


async def get_news_count(db: AsyncSession, category_id: int):
    stmt = select(func.count(News.id)).where(News.category_id == category_id)
    result = await db.execute(stmt)
    return result.scalar_one()


async def get_news_detail(db: AsyncSession, news_id: int):
    # Try cache first.
    cached_news = await get_cached_news_detail(news_id)
    if cached_news is not None:
        # Cached data may include related_news, which is not a News model field.
        # filtered_data = {k: v for k, v in cached_news.items() if k != 'related_news'}
        # return News(**filtered_data)
        return News(**cached_news)

    stmt = select(News).where(News.id == news_id)
    result = await db.execute(stmt)
    news = result.scalar_one_or_none()

    if news:
        # Store database-style field names in cache.
        # news_dict = {k: v for k, v in news.__dict__.items() if not k.startswith('_')}
        news_dict = NewsDetailResponse.model_validate(news).model_dump(
            by_alias=False, mode="json", exclude={'related_news'}
        )
        await cache_news_detail(news_id, news_dict)

    return news


async def increase_news_views(db: AsyncSession, news_id: int):
    stmt = update(News).where(News.id == news_id).values(views=News.views + 1)
    result = await db.execute(stmt)
    await db.commit()

    # Return True when an existing row was updated.
    return result.rowcount > 0


async def get_related_news(db: AsyncSession, news_id: int, category_id: int, limit: int = 5):
    cached_related = await get_cached_related_news(news_id, category_id)
    if cached_related is not None:
        return cached_related

    stmt = select(News).where(
        News.category_id == category_id,
        News.id != news_id
    ).order_by(
        News.views.desc(),
        News.publish_time.desc()
    ).limit(limit)
    result = await db.execute(stmt)
    # return result.scalars().all()
    related_news = result.scalars().all()

    # Store database-style field names in cache, including empty result sets.
    related_data = [
        RelatedNewsResponse.model_validate(news).model_dump(by_alias=False, mode="json")
        for news in related_news
    ]
    await cache_related_news(news_id, category_id, related_data)
    return related_data
    # return [{
    #     "id": news_detail.id,
    #     "title": news_detail.title,
    #     "content": news_detail.content,
    #     "image": news_detail.image,
    #     "author": news_detail.author,
    #     "publishTime": news_detail.publish_time,
    #     "categoryId": news_detail.category_id,
    #     "views": news_detail.views
    # } for news_detail in related_news]
