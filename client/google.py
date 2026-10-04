from dataclasses import dataclass 
from schema import GoogleUserData
from settings import Settings
import httpx


@dataclass
class GoogleClient:
    settings: Settings

    async def get_user_info(self, code: str) -> GoogleUserData:
        data = {
            'code' : code,
            'client_id' : self.settings.GOOGLE_CLIENT_ID,
            'client_secret' : self.settings.GOOGLE_CLIENT_SECRET,
            'redirect_uri' : self.settings.GOOGLE_REDIRECT_URI,
            'grant_type' : 'authorization_code',
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.settings.GOOGLE_TOKEN_URL, 
                data=data
            )
        access_token = response.json().get('access_token')

        async with httpx.AsyncClient() as client:
            user_info = await client.get(
                'https://www.googleapis.com/oauth2/v1/userinfo',
                headers={'Authorization' : f'Bearer {access_token}'}
            )
            
        return GoogleUserData(**user_info.json(), access_token=access_token)
 