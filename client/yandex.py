import base64
from dataclasses import dataclass
from schema.auth import YandexUserData
from settings import Settings
import requests


@dataclass
class YandexClient:
    settings: Settings

    def get_user_info(self, code: str) -> YandexUserData :
        response = requests.post(
            self.settings.YANDEX_TOKEN_URL,
            data = {
                'grant_type': 'authorization_code',
                'code': code,
                'client_id': self.settings.YANDEX_CLIENT_ID,
                'client_secret': self.settings.YANDEX_CLIENT_SECRET,
            },
            headers = {'Conetent_type': 'application/x-www-form-urlencoded'}
        )
        accesss_token = response.json().get('access_token')
        user_info = requests.get(
            'https://login.yandex.ru/info?format=json',
            headers={'Authorization': f'OAuth {accesss_token}'}
        )
        return YandexUserData(**user_info.json(), access_token=accesss_token)
        
    
   