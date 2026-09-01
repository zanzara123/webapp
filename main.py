import uvicorn
from fastapi import FastAPI

from handlers import routers

app = FastAPI()

for router in routers:
    app.include_router(router)



@app.get("/")
def main():
    return {"message" : "ok"}


if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)
