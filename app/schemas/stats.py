from pydantic import BaseModel


class HeroStatsResponse(BaseModel):
    hero_id: int
    hero_name: str
    games: int
    wins: int
    losses: int
    win_rate: float

class PlayerStatsResponse(BaseModel):
    games: int
    wins: int
    losses: int
    win_rate: float
    avg_kills: float
    avg_deaths: float
    avg_assists: float