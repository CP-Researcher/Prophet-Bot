import sys 
sys.path.append('..')
import settings 

from discord.ext import commands
from discord import FFmpegPCMAudio
from os import path
from os import listdir
import os 
from random import choice
import asyncio

last = None
bot = commands.Bot(command_prefix=['clip!', 'c!'])

@bot.event
async def on_ready():
    print("I'm ready to go!")

@bot.command(aliases=["p"])
async def play(ctx, *args): 
    if len(args) == 0 or ctx.author.voice is None:
        if len(args) == 0:
            print("No args, idiot.")
        if ctx.author.voice is None: 
            print("Connect to voice, idiot.")
        return 
    file = '../clips/' + args[0] + '.mp3'
    if not path.exists(file):
        print(os.getcwd())
        print("No such file (" + args[0] + ".mp3)")
        await ctx.reply(args[0] + " does not exists.")
        return 
    global last 
    last = args[0]
    user_channel = ctx.author.voice.channel

  
    voice_client = None 
    if ctx.me.voice is None or ctx.me.voice.channel != user_channel:
        voice_client = await user_channel.connect() 

    voice_client.play(FFmpegPCMAudio(file))
    while voice_client.is_playing(): 
        await(asyncio.sleep(0.2))
    
    try:
        if ctx.me.voice.channel is not None:
            await voice_client.disconnect() 
    except AttributeError:
        pass 

@bot.command(aliases=["r"])
async def random(ctx):
    r = choice(listdir("../clips"))
    r = r[:-4]
    await play(ctx, r)

@bot.command(aliases=["re"])
async def replay(ctx):
    if last is None: 
        return 
    await play(ctx, last)

@bot.event
async def on_voice_state_update(member, before, after) :

    if before.channel is None and after.channel is not None and not member.bot:
        voice_client = await after.channel.connect() 
        voice_client.play(FFmpegPCMAudio("../clips/voice01.mp3"))
        while voice_client.is_playing(): 
            await(asyncio.sleep(0.2))
        try:
            if voice_client.channel is not None:
                await voice_client.disconnect() 
        except AttributeError:
            pass 

    
        

bot.run(settings.DISCORD_TOKEN)
