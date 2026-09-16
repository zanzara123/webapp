from dataclasses import dataclass 
from schema import GoogleUserData
from settings import Settings
import requests


@dataclass
class GoogleClient:
    settings: Settings

    def get_user_info(self, code: str) -> GoogleUserData:
        data = {
            'code' : code,
            'client_id' : self.settings.GOOGLE_CLIENT_ID,
            'client_secret' : self.settings.GOOGLE_CLIENT_SECRET,
            'redirect_uri' : self.settings.GOOGLE_REDIRECT_URI,
            'grant_type' : 'authorization_code',
        }
        response = requests.post(self.settings.GOOGLE_TOKEN_URL, data=data)
        access_token = response.json().get('access_token')

        user_info = requests.get(
            'https://www.googleapis.com/oauth2/v1/userinfo',
            headers={'Authorization' : f'Bearer {access_token}'}
        )
        return GoogleUserData(**user_info.json(), access_token=access_token)
 