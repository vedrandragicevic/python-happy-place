import asyncio
import aiohttp
import ssl
import requests
import urllib3
urllib3.disable_warnings()


async def get_request_async(session, url, headers):
    async with session.get(url, headers=headers, ssl=False) as response:
        return await response.json()


async def fetch_all(urls, loop, headers):
    async with aiohttp.ClientSession(loop=loop) as session:
        results = await asyncio.gather(*[get_request_async(session, url, headers) for url in urls], return_exceptions=True)
        return results


async def patch_request_async(session, url, headers, payload):
    async with session.patch(url, headers=headers, json=payload, ssl=False) as response:
        return await response.json()


async def patch_all(urls, loop, headers, payload):
    async with aiohttp.ClientSession(loop=loop) as session:
        results = await asyncio.gather(*[patch_request_async(session, url, headers, payload) for url in urls], return_exceptions=True)
        return results


async def post_request_async(url, session, headers, body):
    async with session.post(url, headers=headers, json=body) as response:
        return await response.json()


async def post_all(urls, loop, headers, payload):
    async with aiohttp.ClientSession(loop=loop) as session:
        results = await asyncio.gather(*[post_request_async(session, url, headers, payload) for url in urls], return_exceptions=True)
        return results


if __name__ == '__main__':
    token = "123abc"
    api_call_headers = {'Authorization': 'Bearer ' + token}

    # A LIST OF GET/POST/PATCH URLS
    urls = []

    # Async GET REQUEST
    loop = asyncio.get_event_loop()
    responses_list = loop.run_until_complete(fetch_all(urls, loop, api_call_headers))

    for get_request_response in responses_list:
        print(f"GET REQUEST RESPONSE: {get_request_response}")

    # PATCH PAYLOAD
    payload = {"fields": {"field1": {"value": "vexify"}}}

    # Async PATCH REQUEST
    loop = asyncio.get_event_loop()
    patch_responses_list = loop.run_until_complete(patch_all(urls, loop, api_call_headers, payload))

    for patch_response in patch_responses_list:
        print(f"PATCH REQUEST RESPONSE: {patch_response}")
