import sys 
sys.path.append('..')
from discord.ext import commands
from discord import FFmpegPCMAudio, Embed

import os 
import json 
import asyncio
import settings 

from random import choice
from os import path
from os import listdir
from gtts import gTTS

last = None

try:
    with open('sentence_mapper.json', 'r') as f:
        sentence_mapper = json.load(f)
except:
    print('Please create sentence_mapper.json')
    exit()


bot = commands.Bot(command_prefix=['clip!', 'c!', '?'])


@bot.event
async def on_ready():
    """
    First greeting when the bot comes up
    """
    print("I'm ready to go!")
    
    
@bot.command(aliases=["p"])
async def play(ctx, *args):
    """
    Play sounds
    
    Example: `?p สวัสดีครับ`
    """
    if len(args) == 0 or ctx.author.voice is None:
        if len(args) == 0:
            print("No args, idiot.")
        if ctx.author.voice is None: 
            print("Connect to voice, idiot.")
        return 
    if args[0] == 'help':
        text = ", ".join([f'`{x}`' for x in sentence_mapper.keys()])
        embed = Embed(title='🧐Sasada Teaching Lession', description=text, color=0xae00ff)
        await ctx.send(embed=embed)
        return
    if args[0] not in sentence_mapper.keys():
        print("No this sentence in sentence_mapper")
        await ctx.reply("Not this sentence in list")
        return 
    filename = 'clips/' + sentence_mapper[args[0]]
    if not path.exists(filename):
        print("No such file (" + args[0] + ".mp3)")
        await ctx.reply(args[0] + " does not exists.")
        return 
    global last 
    last = sentence_mapper[args[0]]
    user_channel = ctx.author.voice.channel

    voice_client = None 
    if ctx.me.voice is None or ctx.me.voice.channel != user_channel:
        voice_client = await user_channel.connect() 
        
    voice_client.play(FFmpegPCMAudio(executable="ffmpeg/bin/ffmpeg.exe", source=filename))
    while voice_client.is_playing(): 
        await(asyncio.sleep(0.2))
    
    try:
        if ctx.me.voice.channel is not None:
            await voice_client.disconnect() 
    except AttributeError:
        pass 


@bot.command(aliases=["ls"])
async def get_existing_sentences(ctx):
    """
    List all recorded sounds that can be played
    
    Example: `?ls`
    """
    global sentence_mapper
    embed = Embed(title="Sasada Bot Command List  ", description="wanna learn some Sasada's teaching 👉👌 kiddo?", color=0xae00ff)
    embed.add_field(name="Teaching", value="`?p action`\n", inline=True)
    embed.add_field(name="Cursing", value="`?b name`\nrandomly cursing ur friend", inline=True)
    await ctx.send(embed=embed)
    # await ctx.reply("```python\n Existing sentences\n{}```".format('\n'.join([sentence for sentence in sentence_mapper])))


SENTENCES = [
    'ไอ้ {name} ไอ้หน้าหี',
    'ไอ้ {name} หัวควย',
    'พ่อมึงตาย ไอ้ {name}',
    'ไอ้ {name} ไอ้ควาย',
    'ไอ้ {name} ไอ้สัส',
    'ไอ้บ้าเอ้ย',
    'อี ดอกทอง {name}',
    'ไอ้สันขวาน {name}',
    'ไอ้ระยำ {name}',
    'ฉันไม่ด่าคุณหรอก คุณ {name}',
]

@bot.command(aliases=["b"])
async def cursing(ctx, *args):
    """
    Curse other people
    
    Example: `?b ทู`
    """
    
    FILENAME = 'curse.mp3'
    
    if len(args) == 0:
        print("No args, idiot.")
        
    name = args[0]
    tts = gTTS(text=choice(SENTENCES).format(name=name), lang='th')
    tts.save(FILENAME)
    user_channel = ctx.author.voice.channel

    voice_client = None 
    if ctx.me.voice is None or ctx.me.voice.channel != user_channel:
        voice_client = await user_channel.connect() 
        
    voice_client.play(FFmpegPCMAudio(executable="ffmpeg/bin/ffmpeg.exe", source=FILENAME))
    while voice_client.is_playing(): 
        await(asyncio.sleep(0.2))
    
    try:
        if ctx.me.voice.channel is not None:
            await voice_client.disconnect() 
    except AttributeError:
        pass 


@bot.command(aliases=["r"])
async def random(ctx):
    r = choice(listdir("clips"))
    r = r[:-4]
    await play(ctx, r)
    
    
@bot.command(aliases=["dc"])
async def discon(ctx):
    server = ctx.message.guild.voice_client
    await server.disconnect()


@bot.command(aliases=["re"])
async def replay(ctx):
    if last is None: 
        return 
    await play(ctx, last)


@bot.event
async def on_voice_state_update(member, before, after) :

    if before.channel is None and after.channel is not None and not member.bot:
        voice_client = await after.channel.connect() 
        voice_client.play(FFmpegPCMAudio("clips/{}.mp3".format(sentence_mapper["สวัสดีครับ"])))
        while voice_client.is_playing(): 
            await(asyncio.sleep(0.2))
        try:
            if voice_client.channel is not None:
                await voice_client.disconnect() 
        except AttributeError:
            pass        

bot.run(settings.DISCORD_TOKEN)
