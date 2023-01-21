import aiohttp
import requests
import asyncio
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse, HTMLResponse
from urllib.parse import unquote
import nest_asyncio
nest_asyncio.apply()
#pip3 uninstall uvloop


app = FastAPI()
loop = asyncio.get_event_loop()


async def getXML(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            result = await resp.text()
        return result.split("\r\n")


def generate(url):
    r = requests.get(url).text
    r = r.split("\n")[0]
    r = r[19:-1].split(",")
    res = []

    tasks = [getXML(i) for i in r]
    tmp = loop.run_until_complete(asyncio.gather(*tasks))

    for i in range(0, len(tmp)):
        if i == 0:
            res.append(tmp[i][0])
        res.extend(tmp[i][1:-1])
        if i == len(r) - 1:
            res.append(tmp[i][-1])

    return "\n".join(res)


@app.get("/", response_class=HTMLResponse)
async def root(url: str):
    url = unquote(url)
    return generate(url)
