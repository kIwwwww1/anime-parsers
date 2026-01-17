import httpx
from url_params import BaseSearchModel

class _HTTPCLIENT():

    '''Синхронный вариант AsyncExecutor'''


    _instance = None
    client: httpx.Client

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.client = httpx.Client()
        return cls._instance
    
    def close(self):
        self.client.close()


class SyncExecutor():

    '''Синхронный вариант SyncExecutor'''

    def __init__(self, _x_api_key: str, client: httpx.Client):
        self._x_api_key = _x_api_key
        self._client = client
        self._base_url = 'https://kinopoiskapiunofficial.tech/api/v2.1/films'


    def search_media(self, keyword: str, page: int = 20):
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


def main():
    http_client = _HTTPCLIENT()
    ex = SyncExecutor('672174fa-fef0-4fc5-bf60-65d950dcb0a1', http_client.client)
    result = ex.search_media('магическая битва', 1)
    print(result)
    http_client.close()


if __name__ == '__main__':
    main()
