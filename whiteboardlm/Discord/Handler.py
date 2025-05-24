import discord
from whiteboardlm.Common import respond
from whiteboardlm.Discord import DiscordEventObject


def discord_start(discord_token: str, uid: str):
    intents = discord.Intents.all()
    client = discord.Client(intents=intents)

    def to_bot(obj: DiscordEventObject) -> bool:
        return obj.author != client.user or client.user in obj.mentions

    @client.event
    async def on_ready():
        print('Bot ready')

    @client.event
    async def on_message(message):
        obj = DiscordEventObject(message)

        if to_bot(obj):
            result = respond(obj.message, uid)
            await obj.channel.send(result)

    client.run(discord_token)
