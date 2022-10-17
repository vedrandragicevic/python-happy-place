""" EXAMPLE SCRIPT OF A FAST API ENDPOINT WHICH USES ASYNCIO GET REQUEST. """
import asyncio
import aiohttp
import ssl
import requests
import urllib3
urllib3.disable_warnings()


def get_tasks(session, urls, headers):
    tasks = []
    for url in urls:
        tasks.append(session.get(url, headers=headers, ssl=False))
    return tasks


async def fetch_all(urls, headers, loop):
    results = []
    async with aiohttp.ClientSession(loop=loop) as session:
        tasks = get_tasks(session, urls, headers)
        responses = await asyncio.gather(*tasks)
        for response in responses:
            results.append(await response.json())
    return results


async def put_endpoint_example_(put_payload: put_payload):
    list_of_get_urls = []

    token = "123abc"
    headers = {'Authorization': 'Bearer ' + token}

    loop = asyncio.get_event_loop()
    get_responses_list = await (fetch_all(list_of_get_urls, headers, loop))
    for response in get_responses_list:
        print(response)
