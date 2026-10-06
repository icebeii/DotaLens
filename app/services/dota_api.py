import httpx
from app.services.exceptions import DotaApiError, PlayerNotFoundError

class DotaApiClient:
    BASE_URL = "https://api.opendota.com/api"

    async def get_player(self, steam_id: int):
        url = f"{self.BASE_URL}/players/{steam_id}"

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url)

            if response.status_code == 404:
                raise PlayerNotFoundError

            response.raise_for_status()
            return response.json()

        except httpx.HTTPError as error:
            raise DotaApiError from error

    async def get_player_matches(self, steam_id: int, limit: int = 20):
        url = f"{self.BASE_URL}/players/{steam_id}/matches"

        params = {
            "limit": limit,
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params)

            if response.status_code == 404:
                raise PlayerNotFoundError

            response.raise_for_status()
            return response.json()

        except httpx.HTTPError as error:
            raise DotaApiError from error

    async def get_heroes(self):
        url = f"{self.BASE_URL}/heroes"

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url)

            response.raise_for_status()
            return response.json()

        except httpx.HTTPError as error:
            raise DotaApiError from error