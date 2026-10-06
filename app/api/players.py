from fastapi import APIRouter, HTTPException

from app.services.dota_api import DotaApiClient
from app.services.exceptions import DotaApiError, PlayerNotFoundError
from app.services.match_service import calculate_win, get_hero_name, calculate_hero_stats, calculate_player_stats
from app.schemas.player import PlayerResponse
from app.schemas.match import MatchResponse
from app.schemas.stats import HeroStatsResponse, PlayerStatsResponse


router = APIRouter(
    prefix="/api/v1/players",
    tags=["Players"],
)

dota_api = DotaApiClient()

@router.get("/{steam_id}", response_model=PlayerResponse)
async def get_player(steam_id: int):
    try:
        player = await dota_api.get_player(steam_id)

    except PlayerNotFoundError:
        raise HTTPException(status_code=404, detail="Player not found")

    except DotaApiError:
        raise HTTPException(status_code=502, detail="Dota API is unavailable")

    profile = player.get("profile")
    if not profile:
        raise HTTPException(status_code=404, detail="Player not found")

    return {
        "steam_id": profile["account_id"],
        "personaname": profile["personaname"],
        "profile_url": profile["profileurl"],
        "avatar": profile["avatar"],
        "avatarfull": profile["avatarfull"],
    }

@router.get("/{steam_id}/matches", response_model=list[MatchResponse])
async def get_player_matches(steam_id: int, limit: int = 20):
    try:
        matches = await dota_api.get_player_matches(steam_id, limit)
        heroes = await dota_api.get_heroes()

    except PlayerNotFoundError:
        raise HTTPException(status_code=404, detail="Player not found")

    except DotaApiError:
        raise HTTPException(status_code=502, detail="Dota API is unavailable")

    result = []
    for match in matches:
        result.append(
            {
                "match_id": match["match_id"],
                "hero_id": match["hero_id"],
                "hero_name": get_hero_name(
                    heroes,
                    match["hero_id"],
                ),
                "kills": match["kills"],
                "deaths": match["deaths"],
                "assists": match["assists"],
                "win": calculate_win(
                    match["player_slot"],
                    match["radiant_win"],
                )
            }
        )

    return result

@router.get("/{steam_id}/heroes", response_model=list[HeroStatsResponse])
async def get_player_heroes(steam_id: int, limit: int = 100):
    try:
        matches = await dota_api.get_player_matches(steam_id, limit)
        heroes = await dota_api.get_heroes()

    except PlayerNotFoundError:
        raise HTTPException(status_code=404, detail="Player not found")

    except DotaApiError:
        raise HTTPException(status_code=502, detail="Dota API is unavailable")

    return calculate_hero_stats(matches, heroes)

@router.get("/{steam_id}/stats", response_model=PlayerStatsResponse)
async def get_player_stats(steam_id: int, limit: int = 100):
    try:
        matches = await dota_api.get_player_matches(steam_id, limit)

    except PlayerNotFoundError:
        raise HTTPException(status_code=404, detail="Player not found")

    except DotaApiError:
        raise HTTPException(status_code=502, detail="Dota API is unavailable")

    return calculate_player_stats(matches)