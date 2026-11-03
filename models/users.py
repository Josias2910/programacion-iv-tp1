from pydantic import BaseModel, ConfigDict, Field


class UserData(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(min_length=1, max_length=100)
    is_active: bool = True


class User(UserData):
    id: int = Field(gt=0)


class GetUsersResponse(BaseModel):
    users: list[User]


class MessageResponse(BaseModel):
    message: str
