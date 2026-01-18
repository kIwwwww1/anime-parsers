import asyncio
from os import getenv
from dotenv import load_dotenv
from assets.main_assets.respons import A_HTTPCLIENT
from assets.kinopoisk.async_pars import AsyncExecutor

load_dotenv()

secret_key = getenv('SECRET_KEY')



async def main():
    http_client = A_HTTPCLIENT()
    ex = AsyncExecutor(secret_key, http_client.client)
    result = await ex.a_get_filters_media(genres_id=24, keyword='Магическая битва', page=1)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())