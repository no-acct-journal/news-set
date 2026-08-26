from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Enum, ForeignKey, Index, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    """User profile ORM model."""

    __tablename__ = "user"

    __table_args__ = (
        Index("username_UNIQUE", "username"),
        Index("phone_UNIQUE", "phone"),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="User ID",
    )

    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        comment="Username",
    )

    password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="Hashed password",
    )

    nickname: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        comment="Nickname",
    )

    avatar: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        default="https://fastly.jsdelivr.net/npm/@vant/assets/cat.jpeg",
        comment="Avatar URL",
    )

    gender: Mapped[Optional[str]] = mapped_column(
        Enum("male", "female", "unknown", name="user_gender_enum"),
        nullable=True,
        default="unknown",
        comment="Gender",
    )

    bio: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
        default="This user has not added a bio yet.",
        comment="Bio",
    )

    phone: Mapped[Optional[str]] = mapped_column(
        String(20),
        unique=True,
        nullable=True,
        comment="Phone number",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        nullable=False,
        comment="Created at",
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now,
        nullable=False,
        comment="Updated at",
    )

    def __repr__(self) -> str:
        return (
            f"<User("
            f"id={self.id}, "
            f"username='{self.username}', "
            f"nickname='{self.nickname}'"
            f")>"
        )


class UserToken(Base):
    """User token ORM model."""

    __tablename__ = "user_token"

    __table_args__ = (
        Index("token_UNIQUE", "token"),
        Index("fk_user_token_user_idx", "user_id"),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="Token ID",
    )

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("user.id"),
        nullable=False,
        comment="User ID",
    )

    token: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        comment="Token value",
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        comment="Expiration time",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        nullable=False,
        comment="Created at",
    )

    def __repr__(self) -> str:
        return (
            f"<UserToken("
            f"id={self.id}, "
            f"user_id={self.user_id}, "
            f"token='{self.token}'"
            f")>"
        )
