# Cache helpers for news categories, lists, details, and related news.
# key - value
from typing import List, Dict, Any, Optional

from config.cache_conf import get_json_cache, set_cache

CATEGORIES_KEY = "news:categories"
NEWS_LIST_PREFIX = "news_list:"
NEWS_DETAIL_PREFIX = "news:detail:"
RELATED_NEWS_PREFIX = "news:related:"


# Get cached news categories.
async def get_cached_categories():
    return await get_json_cache(CATEGORIES_KEY)


# Cache stable data longer and keep volatile data shorter.
async def set_cache_categories(data: List[Dict[str, Any]], expire: int = 7200):
    return await set_cache(CATEGORIES_KEY, data, expire)


# Cache a news list. Key format: news_list:{category_id}:{page}:{size}.
async def set_cache_news_list(category_id: Optional[int], page: int, size: int, news_list: List[Dict[str, Any]], expire: int = 1800):
    category_part = category_id if category_id is not None else "all"
    key = f"{NEWS_LIST_PREFIX}{category_part}:{page}:{size}"
    return await set_cache(key, news_list, expire)


# Get a cached news list.
async def get_cache_news_list(category_id: Optional[int], page: int, size: int):
    category_part = category_id if category_id is not None else "all"
    key = f"{NEWS_LIST_PREFIX}{category_part}:{page}:{size}"
    return await get_json_cache(key)


async def get_cached_news_detail(news_id: int) -> Optional[Dict[str, Any]]:
    """
    Get cached news detail.

    Args:
        news_id: News ID.

    Returns:
        Optional[Dict[str, Any]]: News data, or None when not cached.
    """
    key = f"{NEWS_DETAIL_PREFIX}{news_id}"
    return await get_json_cache(key)


async def cache_news_detail(news_id: int, news_data: Dict[str, Any], expire: int = 300) -> bool:
    """
    Cache news detail.

    Args:
        news_id: News ID.
        news_data: News data dictionary.
        expire: Expiration in seconds. Defaults to 5 minutes.

    Returns:
        bool: True if the cache write succeeds.
    """
    key = f"{NEWS_DETAIL_PREFIX}{news_id}"
    return await set_cache(key, news_data, expire)


async def cache_related_news(news_id: int, category_id: int, related_list: List[Dict[str, Any]], expire: int = 1800) -> bool:
    """
    Cache related news.

    Args:
        news_id: Current news ID.
        category_id: News category ID.
        related_list: Related news list.
        expire: Expiration in seconds.

    Returns:
        bool: True if the cache write succeeds.
    """
    key = f"{RELATED_NEWS_PREFIX}{news_id}:{category_id}"
    return await set_cache(key, related_list, expire)


async def get_cached_related_news(news_id: int, category_id: int) -> Optional[List[Dict[str, Any]]]:
    """
    Get cached related news.

    Args:
        news_id: Current news ID.
        category_id: News category ID.

    Returns:
        Optional[List[Dict[str, Any]]]: Related news list, or None when not cached.
    """
    key = f"{RELATED_NEWS_PREFIX}{news_id}:{category_id}"
    return await get_json_cache(key)
