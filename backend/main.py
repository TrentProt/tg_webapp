import logging

from fastapi import HTTPException, Query
from fastapi.responses import JSONResponse

from backend.app_init import create_app
from backend.config import CONFIG
from backend.data import CONTAINERS
from backend.utils import validate_init_data


logger = logging.getLogger(__name__)

BOT_TOKEN = CONFIG.tgbot.api_key

app = create_app()


@app.get('/containers')
def get_containers(initData: str = Query(...)):
    '''
    GET эндпоинт для получения контейнеров.
    initData передается как query-параметр.
    '''
    logger.info(f'GET /containers вызван с initData: {initData[:50]}...')

    if not validate_init_data(initData, BOT_TOKEN):
        logger.error('Валидация не пройдена!')
        raise HTTPException(status_code=403, detail='Invalid initData')

    logger.info('Валидация пройдена успешно!')
    return JSONResponse(content=CONTAINERS)


@app.get('/container/{container_id}')
def get_container(
        container_id: int,
        initData: str = Query(...)
):
    '''
    GET эндпоинт для получения конкретного контейнера по ID.
    initData передается как query-параметр.
    '''
    logger.info(f'GET /container/{container_id} вызван с initData: {initData[:50]}...')

    if not validate_init_data(initData, BOT_TOKEN):
        logger.error('Валидация не пройдена для контейнера!')
        raise HTTPException(status_code=403, detail='Invalid initData')

    logger.info(f'Валидация пройдена. Ищем контейнер с ID={container_id}')

    for container in CONTAINERS:
        if container['id'] == container_id:
            logger.info(f'Контейнер {container_id} найден: {container["name"]}')
            return JSONResponse(content=container)

    logger.error(f'Контейнер с ID={container_id} не найден')
    raise HTTPException(status_code=404, detail=f'Container with ID {container_id} not found')

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(
        app,
        host=CONFIG.fastapi.host,
        port=CONFIG.fastapi.port,
        reload=CONFIG.fastapi.reload
    )
