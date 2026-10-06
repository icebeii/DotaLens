from pydantic import BaseModel


class MatchResponse(BaseModel):
    match_id: int
    hero_id: int
    hero_name: str
    kills: int
    deaths: int
    assists: int
    win: bool