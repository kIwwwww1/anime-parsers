import httpx
from loguru import logger

class A_HTTPCLIENT():

    '''Асинхронный вариант кода'''

    _instance = None
    client: httpx.AsyncClient

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.client = httpx.AsyncClient()
        return cls._instance
    
    async def close(self):
        await self.client.aclose()


