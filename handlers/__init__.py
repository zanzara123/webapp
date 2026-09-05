from handlers.catalog import router as catalog_router
from handlers.user import router as user_router
from handlers.auth import router as auth_router


routers = [catalog_router, user_router, auth_router]