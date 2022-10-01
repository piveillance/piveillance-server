# no idea if this works or even what it does

import aiohttp
import asyncio

async def handle(request):
    name = request.match_info.get('name', "Anonymous")
    discord_id = name
    return web.Response(text=discord_id)

app = web.Application()
app.add_routes([web.get('/', handle),
                web.get('/{name}', handle)])
