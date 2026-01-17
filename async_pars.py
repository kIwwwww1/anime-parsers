from os import getenv
from dotenv import load_dotenv
from loguru import logger
import asyncio
import httpx
from url_params import (BaseSearchModel, MediaId)
from pydantic import ValidationError
from json import JSONDecodeError

load_dotenv()

secret_key = getenv('SECRET_KEY')

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


class AsyncExecutor():

    '''Асинхронный вариант AsyncExecutor'''

    def __init__(self, _x_api_key: str, client: httpx.AsyncClient):
        self._x_api_key = _x_api_key
        self._client = client
        self._base_url = 'https://kinopoiskapiunofficial.tech/api/v2.1/films'
        self._new_base_url = 'https://kinopoiskapiunofficial.tech/api/v2.2/films'


    async def a_get(self, url: str, 
                    params: dict | None = None,
                    headers: dict | None = None):
        try:
            resp = (await self._client.get(url=url, params=params,headers=headers)).json()
            return resp
        finally:
            logger.debug('Соединение закрыто в finally')
            await self._client.aclose()


    async def a_search_media(self, keyword: str, page: int):
        '''
        {
            "keyword": "Название",           (Поисковый запрос, который вы отправили)
            "pagesCount": 1,                 (Номер страницы, на 1 странице 20 записей)
            "films": [ ... ],                (Список объектов с информацией о каждом фильме/сериале)
            "searchFilmsCountResult": 160    (Общее количество результатов)
        }
        '''
        try:
            params = BaseSearchModel(keyword=keyword, page=page).model_dump()
            resp: dict = await self.a_get(
                url=self._base_url + '/search-by-keyword',
                params=params,
                headers={'X-API-KEY': self._x_api_key},
            )
            if resp:
                return resp
        except ValidationError:
            return {'error': 'Keyword и ID не может быть < 1'}



    async def a_get_media_by_id(self, media_id: int):
        '''
        {
            'kinopoiskId': int,
            'kinopoiskHDId': str | None,
            'imdbId': str | None,
            'nameRu': str | None,
            'nameEn': str | None,
            'nameOriginal': str | None,
            'posterUrl': str | None,
            'posterUrlPreview': str | None,
            'coverUrl': str | None,
            'logoUrl': str | None,
            'reviewsCount': int,
            'ratingGoodReview': float | None,
            'ratingGoodReviewVoteCount': int,
            'ratingKinopoisk': float | None,
            'ratingKinopoiskVoteCount': int,
            'ratingImdb': float | None,
            'ratingImdbVoteCount': int,
            'ratingFilmCritics': float | None,
            'ratingFilmCriticsVoteCount': int,
            'ratingAwait': float | None,
            'ratingAwaitCount': int,
            'ratingRfCritics': float | None,
            'ratingRfCriticsVoteCount': int,
            'webUrl': str | None,
            'year': int | None,
            'filmLength': int | None,
            'slogan': str | None,
            'description': str | None,
            'shortDescription': str | None,
            'editorAnnotation': str | None,
            'isTicketsAvailable': bool,
            'productionStatus': str | None,
            'type': str,
            'ratingMpaa': str | None,
            'ratingAgeLimits': str | None,
            'countries': list[dict[str, str]],
            'genres': list[dict[str, str]],
            'startYear': int | None,
            'endYear': int | None,
            'serial': bool,
            'shortFilm': bool,
            'completed': bool,
            'hasImax': bool,
            'has3D': bool,
            'lastSync': str  # ISO 8601 формат: "YYYY-MM-DDTHH:MM:SS.ffffff"
        }
        '''
        try:
            params = MediaId(id=media_id).model_dump()
            endpoint_url = f'{self._new_base_url}/{params.get('id')}'
            resp = await self.a_get(
                url=endpoint_url,
                params=params,
                headers={'X-API-KEY': self._x_api_key})
            if resp:
                return resp
        except JSONDecodeError:
            return {'error': 'Сервер вернул 404'}
        except ValidationError:
            return {'error': 'ID не может быть < 1'}


    async def a_get_financials(self, media_id: int):
        try:
            params = MediaId(id=media_id).model_dump()
            endpoint_url = f'{self._new_base_url}/{params.get('id')}/box_office'
            resp = await self.a_get(
                url=endpoint_url,
                params=params,
                headers={'X-API-KEY': self._x_api_key})
            return resp
        except ValidationError:
            return {'error': 'ID не может быть < 1'}


async def a_main():
    http_client = A_HTTPCLIENT()
    ex = AsyncExecutor(secret_key, http_client.client)
    result = await ex.a_search_media('Атака титанов', 1)
    # result = await ex.a_get_media_by_id(14124)
    # result = await ex.a_get_financials(1242365)
    print(result)


if __name__ == '__main__':
    asyncio.run(a_main())
