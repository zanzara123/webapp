from dataclasses import dataclass
from client import GoogleClient, YandexClient
from models import UserProfile
from schema import UserLoginSchema, UserCreateSchema

from repository import UserRepository
from exception import UserNotFoundException, UserNotCorrectPasswordException, TokenExpireException, TokenNotCorrectException

from jose import JWTError, jwt

import datetime
from datetime import timedelta
from settings import Settings

@dataclass
class AuthService:
    user_repository: UserRepository
    settings: Settings
    google_client: GoogleClient
    yandex_client: YandexClient

    def google_auth(self, code: str):
        user_data = self.google_client.get_user_info(code)
    
        if user := self.user_repository.get_user_by_email(email=user_data.email):
            access_token = self.generate_access_token(user_id= user.id)
            print('user_login')
            return UserLoginSchema(user_id=user.id, access_token=access_token)
    
        create_user_data = UserCreateSchema(
            google_access_token = user_data.access_token, 
            email=user_data.email,
            name = user_data.name
        )
        created_user = self.user_repository.create_user(create_user_data)
        access_token = self.generate_access_token(user_id= created_user.id)
        print('user_create')
        return UserLoginSchema(user_id=created_user.id, access_token=access_token)


    def yandex_auth(self, code: str):
        user_data = self.yandex_client.get_user_info(code)
        print('user_data :', user_data)

        if user := self.user_repository.get_user_by_email(email=user_data.default_email):
            access_token = self.generate_access_token(user_id= user.id)
            print('user_login')
            return UserLoginSchema(user_id=user.id, access_token=access_token)
            
        create_user_data = UserCreateSchema(
            yandex_access_token = user_data.access_token, 
            email=user_data.default_email,
            name = user_data.name
        )
        created_user = self.user_repository.create_user(create_user_data)
        access_token = self.generate_access_token(user_id= created_user.id)
        print('user_create')
        return UserLoginSchema(user_id=created_user.id, access_token=access_token)
    
    
    def get_google_redirect_url(self) -> str:
        return self.settings.google_redirect_url


    def get_yandex_redirect_url(self) -> str:
        return self.settings.yandex_redirect_url


    def login(self, username: str, password: str) -> UserLoginSchema:
        user: UserProfile= self.user_repository.get_user_by_username(username)
        self._validate_auth_user(user, password)
        access_token = self.generate_access_token(user_id= user.id)
        return UserLoginSchema(user_id=user.id, access_token=access_token)


    def generate_access_token(self, user_id: int) -> str:
        expires_date_unix = (datetime.datetime.now() + timedelta(7)).timestamp()
        token = jwt.encode(
            claims= {'user_id' : user_id, 'expire' : expires_date_unix},
            key = self.settings.JWT_SECRET_KEY,
            algorithm = self.settings.JWT_ENCODE_ALGORITHM
        )
        return token


    def get_user_id_from_access_token(self, access_token: str) -> int:
        try:
            payload = jwt.decode(
                        token = access_token,
                        key = self.settings.JWT_SECRET_KEY,
                        algorithms = self.settings.JWT_ENCODE_ALGORITHM
            )
        except JWTError:
            raise TokenNotCorrectException

        if payload['expire'] < datetime.datetime.now().timestamp():
            raise TokenExpireException
        
        return payload['user_id']
        

    @staticmethod
    def _validate_auth_user(user: UserProfile, password: str):
        if not user:
            raise UserNotFoundException

        if user.password != password:
            raise UserNotCorrectPasswordException
