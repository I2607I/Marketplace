import aiohttp
import json

# получает курс рубля к доллару
async def converter():
    async with aiohttp.ClientSession() as session:
        url = 'http://www.cbr-xml-daily.ru/daily_json.js'
        async with session.get(url) as resp:
            response = await resp.read()
            data = json.loads(response)
            return data['Valute']['USD']['Value']
