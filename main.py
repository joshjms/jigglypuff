import discord
import wavelink
from discord.ext import commands

import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')
LAVALINK_PASSWORD = os.getenv('LAVALINK_PASSWORD')


class Bot(commands.Bot):

    def __init__(self) -> None:
        intents = discord.Intents()
        intents.voice_states = True
        intents.guilds = True
        intents.guild_messages = True
        intents.guild_reactions = True
        intents.messages = True
        intents.reactions = True
        intents.members = True
        intents.presences = True
        super().__init__(intents=intents, command_prefix='/')

    async def on_ready(self) -> None:
        print(f'Logged in {self.user} | {self.user.id}')
        await self.setup_hook()

    async def setup_hook(self) -> None:
        # Wavelink 2.0 has made connecting Nodes easier... Simply create each Node
        # and pass it to NodePool.connect with the client/bot.
        node: wavelink.Node = wavelink.Node(uri='http://localhost:2333', password='youshallnotpass')
        print('Connecting to Lavalink Node...')
        await wavelink.NodePool.connect(client=self, nodes=[node])
        print('Connected to Lavalink Node.')


bot = Bot()


@bot.command()
async def play(ctx: commands.Context, *, search: str) -> None:
    """Simple play command."""

    if not ctx.voice_client:
        vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
    else:
        vc: wavelink.Player = ctx.voice_client

    tracks = await wavelink.YouTubeTrack.search(search)
    if not tracks:
        await ctx.send(f'No tracks found with query: `{search}`')
        return

    track = tracks[0]
    await vc.play(track)


@bot.command()
async def disconnect(ctx: commands.Context) -> None:
    """Simple disconnect command.

    This command assumes there is a currently connected Player.
    """
    vc: wavelink.Player = ctx.voice_client
    await vc.disconnect()
    
bot.run(TOKEN)