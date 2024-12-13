import aiohttp
import json


async def converter():
    async with aiohttp.ClientSession() as session:
        url = 'http://www.cbr-xml-daily.ru/daily_json.js'
        async with session.get(url) as resp:
            response = await resp.read()
            # data = await resp.json(content_type='application/json')
            # print(data)
            data = json.loads(response)
            # print(data['Valute']['USD'])
            return data['Valute']['USD']['Value']

# asyncio.run(converter())
