from typing import Optional

from pydantic import Field, ConfigDict, BaseModel

from schemas.base import NewsItemBase


class RelatedNewsResponse(BaseModel):
    """
    Related news response with only the fields needed by the client.
    """
    id: int
    title: str
    image: Optional[str] = None
    views: int

    model_config = ConfigDict(
        from_attributes=True,
    )


class NewsDetailResponse(NewsItemBase):
    """
    News detail response with content and related news.
    """
    content: str
    related_news: list[RelatedNewsResponse] = Field(default_factory=list, alias="relatedNews")

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )


