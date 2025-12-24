from fastapi import HTTPException

from backend.app_init import create_app
from backend.config import CONFIG
from backend.data import CONTAINERS
from backend.utils import validate_init_data


BOT_TOKEN = CONFIG.tgbot.api_key

app = create_app()

@app.get("/containers")
def get_containers(initData: str):
    # if not validate_init_data(initData, BOT_TOKEN):
    #     raise HTTPException(status_code=403, detail="Invalid initData")
    return CONTAINERS

@app.get("/container/{container_id}")
def get_container(container_id: int, initData: str):
    # if not validate_init_data(initData, BOT_TOKEN):
    #     raise HTTPException(status_code=403, detail="Invalid initData")

    for c in CONTAINERS:
        if c["id"] == container_id:
            return c
    raise HTTPException(status_code=404, detail="Not found")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host=CONFIG.fastapi.host,
        port=CONFIG.fastapi.port,
        reload=CONFIG.fastapi.reload
    )
