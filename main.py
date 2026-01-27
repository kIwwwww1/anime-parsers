import asyncio
from os import getenv
from dotenv import load_dotenv
from assets.main_assets.respons import A_HTTPCLIENT
from assets.kinopoisk.async_pars import AsyncExecutor
from pprint import pprint
from assets.shikimori.async_pars import AsyncExecutor as ShikimoriEx

load_dotenv()

secret_key = getenv('SECRET_KEY')



async def main():
    http_client = A_HTTPCLIENT()
    ex = ShikimoriEx(client=http_client.client)

if __name__ == "__main__":
    asyncio.run(main())


