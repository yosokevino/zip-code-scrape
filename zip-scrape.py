import aiohttp
import asyncio
import pandas as pd

headers = {'accept':'application/json',
          'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'}

zip_data = []

async def make_numbers(numbers, _numbers):
    for i in range(numbers, _numbers):
        str_i = str(i)
        if len(str_i) == 4:
            y = '0'+str_i
        elif len(str_i) == 3:
            y = '00'+str_i
        else:
            y = str_i
        yield y
        
async def do_post(session, url, x):
    async with session.post(url, headers = headers, data = {"zip": str(x)}) as response:
          data = await response.json()
          zip_data.append(data)

async def make_account():
    url = "https://tools.usps.com/tools/app/ziplookup/cityByZip"
    async with aiohttp.ClientSession() as session:
        post_tasks = []
        async for x in make_numbers(1000, 9999):
            post_tasks.append(do_post(session, url, x))
        # now execute them all at once
        await asyncio.gather(*post_tasks)