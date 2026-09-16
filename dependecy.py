from database import get_db_session
from cache import get_redis_connection
from repository import DishRepository, CacheDishRepository, UserRepository
from service import DishService, UserService, AuthService

from sqlalchemy.orm import Session
from settings import Settings

from fastapi import Depends, HTTPException, Request, Security, security

from exception import TokenNotCorrectException, TokenExpireException

from client import GoogleClient, YandexClient


def get_dish_repository(db_session: Session = Depends(get_db_session)) -> DishRepository:
    return DishRepository(db_session)


def get_cache_dish_repository() -> CacheDishRepository:
    redis_connection = get_redis_connection()
    return CacheDishRepository(redis_connection)


def get_dish_service(
    dish_repository: DishRepository = Depends(get_dish_repository),
    dish_cache: CacheDishRepository = Depends(get_cache_dish_repository)
) -> DishService:
    return DishService(
        dish_repository = dish_repository, 
        dish_cache=dish_cache
    )


def get_user_repository(db_session: Session = Depends(get_db_session)) -> UserRepository:
    return UserRepository(db_session=db_session)


def get_google_client() -> GoogleClient:
    return GoogleClient(settings=Settings())

def get_yandex_client() -> YandexClient:
    return YandexClient(settings=Settings())
    

def get_auth_service(
        user_repository: UserRepository = Depends(get_user_repository),
        google_client: GoogleClient = Depends(get_google_client),
        yandex_client: YandexClient = Depends(get_yandex_client)
) -> AuthService:
    return AuthService(user_repository=user_repository, settings=Settings(), google_client=google_client, yandex_client = yandex_client)


def get_user_service(
    user_repository: UserRepository = Depends(get_user_repository),
    auth_service: AuthService = Depends(get_auth_service)
) -> UserService:
    return UserService(user_repository=user_repository, auth_service=auth_service)


reusable_oauth2= security.HTTPBearer()

def get_request_user_id(
        request: Request,
        auth_service: AuthService = Depends(get_auth_service),
        token: security.http.HTTPAuthorizationCredentials = Security(reusable_oauth2),
) -> int:
    try:
        user_id = auth_service.get_user_id_from_access_token(token.credentials)
    except TokenExpireException as e:
        raise  HTTPException(
            status_code=401,
            detail = e.detail
        )
    except TokenNotCorrectException as e:
        raise  HTTPException(
            status_code=401,
            detail = e.detail
        )
    
    return user_id
