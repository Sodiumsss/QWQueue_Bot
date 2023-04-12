import aiohttp

# 参考文档 https://github.com/Sodiumsss/QWQueue_API/wiki/


# 请填写正确的信息。
devToken = "12345678910"
local = False

url = "localhost" if local else "server.qwq.ski"
pre = "http://" if local else "https://"
port = "6325" if local else ""


async def verifyQQ(payload):
    async with aiohttp.request("POST", pre + url + ":" + port + "/dev/QQ/verifyQQ",
                               json=payload, headers={"devToken": devToken}) as resp:
        p = await resp.json()
        return p


async def getGamePlayer(payload):
    async with aiohttp.request("POST", pre + url + ":" + port + "/dev/game/getGamePlayer",
                               json=payload, headers={"devToken": devToken}) as resp:
        p = await resp.json()
        return p

async def incGamePlayer(payload):
    async with aiohttp.request("POST", pre + url + ":" + port + "/dev/game/incGamePlayer",
                               json=payload, headers={"devToken": devToken}) as resp:
        p = await resp.json()
        return p

async def incGamePlayers(payload):
    async with aiohttp.request("POST", pre + url + ":" + port + "/dev/game/incGamePlayers",
                               json=payload, headers={"devToken": devToken}) as resp:
        p = await resp.json()
        return p
async def setGamePlayer(payload):
    async with aiohttp.request("POST", pre + url + ":" + port + "/dev/game/setGamePlayer",
                               json=payload, headers={"devToken": devToken}) as resp:
        p = await resp.json()
        return p

async def decGamePlayer(payload):
    async with aiohttp.request("POST",pre + url + ":" + port + "/dev/game/decGamePlayer",
                               json=payload, headers={"devToken": devToken}) as resp:
        p = await resp.json()
        return p
async def decGamePlayers(payload):
    async with aiohttp.request("POST", pre + url + ":" + port + "/dev/game/decGamePlayers",
                               json=payload, headers={"devToken": devToken}) as resp:
        p = await resp.json()
        return p
async def getSongByAlias(payload):
    async with aiohttp.request("POST", pre + url + ":" + port + "/dev/alias/getSongByAlias",
                               json=payload, headers={"devToken": devToken}) as resp:
        p = await resp.json()
        return p


async def getSongAliases(payload):
    async with aiohttp.request("POST", pre + url + ":" + port + "/dev/alias/getSongAlias",
                               json=payload, headers={"devToken": devToken}) as resp:
        p = await resp.json()
        return p['data']


async def addSongAlias(payload):
    async with aiohttp.request("POST", pre + url + ":" + port + "/dev/alias/addSongAlias",
                               json=payload, headers={"devToken": devToken}) as resp:
        p = await resp.json()
        return p


async def deleteAliasByID(payload):
    async with aiohttp.request("POST", pre + url + ":" + port + "/dev/alias/deleteAliasByID",
                               json=payload, headers={"devToken": devToken}) as resp:
        p = await resp.json()
        if p['code'] == 1:
            return True
        else:
            return False
