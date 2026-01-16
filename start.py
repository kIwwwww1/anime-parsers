import asyncio
import requests
import httpx
# 
from url_params import BaseSearchModel

class _HTTPCLIENT():
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.client = httpx.Client()
        return cls._instance
    
    def close(self):
        self.client.close()



class A_HTTPCLIENT():
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.client = httpx.AsyncClient()
        return cls._instance
    
    async def close(self):
        await self.client.aclose()



class SyncExecutor():

    '''Синхронный вариант кода'''

    def __init__(self, _x_api_key: str, client: httpx.Client):
        self._x_api_key = _x_api_key
        self._client = client
        self._base_url = 'https://kinopoiskapiunofficial.tech/api/v2.1/films'


    def get_anime(self, keyword: str, page: int = 20):
        '''
        {
            "keyword": "Название",           (Поисковый запрос, который вы отправили)
            "pagesCount": 1,                 (Номер страницы, на 1 странице 20 записей)
            "films": [ ... ],                (Список объектов с информацией о каждом фильме/сериале)
            "searchFilmsCountResult": 160    (Общее количество результатов)
        }
        '''
        endpoint_url = '/search-by-keyword'
        params = BaseSearchModel(keyword=keyword, page=page).model_dump()


        resp = self._client.get(
            self._base_url + endpoint_url,
            params=params,
            headers={'X-API-KEY': self._x_api_key},
            )
        data = resp.json()
        return data



# 
class AsyncExecutor():

    '''Асинхронный вариант кода'''

    def __init__(self, _x_api_key: str, client: httpx.AsyncClient):
        self._x_api_key = _x_api_key
        self._client = client
        self._base_url = 'https://kinopoiskapiunofficial.tech/api/v2.1/films'


    async def a_get_anime(self, keyword: str, page: int):
        '''
        {
            "keyword": "Название",           (Поисковый запрос, который вы отправили)
            "pagesCount": 1,                 (Номер страницы, на 1 странице 20 записей)
            "films": [ ... ],                (Список объектов с информацией о каждом фильме/сериале)
            "searchFilmsCountResult": 160    (Общее количество результатов)
        }
        '''
        endpoint_url = '/search-by-keyword'
        params = BaseSearchModel(keyword=keyword, page=page).model_dump()
        resp = await self._client.get(
            self._base_url + endpoint_url,
            params=params,
            headers={'X-API-KEY': self._x_api_key},
            )
        data = resp.json()
        return data


# 


def main():
    http_client = _HTTPCLIENT()
    ex = SyncExecutor('672174fa-fef0-4fc5-bf60-65d950dcb0a1', http_client.client)
    result = ex.get_anime('магическая битва', 1)
    print(result)
    http_client.close()


async def a_main():
    http_client = A_HTTPCLIENT()
    ex = AsyncExecutor('672174fa-fef0-4fc5-bf60-65d950dcb0a1', http_client.client)
    result = await ex.a_get_anime('магическая битва', 1)
    print(result)
    await http_client.close()


if __name__ == '__main__':
    # Запускаем асинхронную версию
    asyncio.run(a_main())
    
    # Запускаем синхронную версию
    main()