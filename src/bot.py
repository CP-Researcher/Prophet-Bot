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
import json 

last = None

try:
    with open('../sentence_mapper.json', 'r') as f:
        sentence_mapper = json.load(f)
except:
    print('Please create sentence_mapper.json')
    exit()


bot = commands.Bot(command_prefix=['clip!', 'c!', '?'])

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
    if args[0] not in sentence_mapper.keys():
        print("No this sentence in sentence_mapper")
        await ctx.reply("Not this sentence in list")
        return 
    file = '../clips/' + sentence_mapper[args[0]]
    if not path.exists(file):
        print("No such file (" + args[0] + ".mp3)")
        await ctx.reply(args[0] + " does not exists.")
        return 
    global last 
    last = sentence_mapper[args[0]]
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

@bot.command(aliases=["ls"])
async def get_existing_sentences(ctx):
    global sentence_mapper
    await ctx.reply("```python\n Existing sentences\n{}```".format('\n'.join([sentence.strip() for sentence in sentence_mapper.keys()])))

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
