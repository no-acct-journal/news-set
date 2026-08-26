from sqlalchemy.orm import Mapped, mapped_column,DeclarativeBase
from sqlalchemy import Integer, DateTime, ForeignKey, Index
from datetime import datetime
from .users import User
from .news import News


class Base(DeclarativeBase):
    pass


class History(Base):
    """
    Browsing history ORM model.
    """
    __tablename__ = 'history'

    __table_args__ = (
        Index('fk_history_user_idx', 'user_id'),
        Index('fk_history_news_idx', 'news_id'),
        Index('idx_view_time', 'view_time'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="History ID")
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey(User.id), nullable=False, comment="User ID")
    news_id: Mapped[int] = mapped_column(Integer, ForeignKey(News.id), nullable=False, comment="News ID")
    view_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False, comment="Viewed at")


    def __repr__(self):
        return f"<History(id={self.id}, user_id={self.user_id}, news_id={self.news_id}, view_time={self.view_time})>"
