from pydantic import BaseModel


class PlayerResponse(BaseModel):
    steam_id: int
    personaname: str | None = None
    profile_url: str | None = None
    avatar: str | None = None
    avatarfull: str | None = None