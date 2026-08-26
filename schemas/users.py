from typing import Optional

from pydantic import BaseModel, Field, ConfigDict

class UserRequest(BaseModel):
    username: str
    password: str

# Base user profile fields used by userInfo responses.
class UserInfoBase(BaseModel):
    """
    Base user profile data model.
    """
    nickname: Optional[str] = Field(None, max_length=50, description="Nickname")
    avatar: Optional[str] = Field(None, max_length=255, description="Avatar URL")
    gender: Optional[str] = Field(None, max_length=10, description="Gender")
    bio: Optional[str] = Field(None, max_length=500, description="Bio")


class UserInfoResponse(UserInfoBase):
    id: int
    username: str

    model_config = ConfigDict(
        from_attributes=True
    )


# Authentication response payload.
class UserAuthResponse(BaseModel):
    token: str
    user_info: UserInfoResponse = Field(..., alias="userInfo")

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )

# User profile update request.
class UserUpdateRequest(BaseModel):
    nickname: str = None
    avatar: str = None
    gender: str = None
    bio: str = None
    phone: str = None

class UserChangePasswordRequest(BaseModel):
    old_password: str = Field(..., alias="oldPassword", description="Old password")
    new_password: str = Field(..., min_length=6, alias="newPassword", description="New password")
