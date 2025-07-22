from aiohttp import web
from botbuilder.core import BotFrameworkAdapter, BotFrameworkAdapterSettings, TurnContext
from botbuilder.schema import Activity
from cyberbot import CyberBot
import asyncio
import json

APP_ID = ""  # Leave blank for emulator
APP_PASSWORD = ""  # Leave blank for emulator

bot = CyberBot()

adapter_settings = BotFrameworkAdapterSettings(APP_ID, APP_PASSWORD)
adapter = BotFrameworkAdapter(adapter_settings)

async def messages(request: web.Request) -> web.Response:
    body = await request.json()
    activity = Activity().deserialize(body)

    async def aux_func(turn_context: TurnContext):
        await bot.on_turn(turn_context)

    await adapter.process_activity(activity, "", aux_func)
    return web.Response(status=200)

app = web.Application()
app.router.add_post("/api/messages", messages)

if __name__ == "__main__":
    web.run_app(app, host="localhost", port=3978)
