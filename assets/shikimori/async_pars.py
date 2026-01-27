from httpx import AsyncClient
from loguru import logger
from json import JSONDecodeError


class AsyncExecutor():

    '''Асинхронный вариант AsyncExecutor'''

    def __init__(self, client: AsyncClient):
        self._client = client
        self._base_url = 'https://shikimori.one/animes'



