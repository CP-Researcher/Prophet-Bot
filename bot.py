import sys 
sys.path.append('..')
from discord.ext import commands
from discord import FFmpegPCMAudio, Embed

import os 
import json 
import asyncio
import settings 

from random import choice, uniform
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
    
voice_client = None 
        
@bot.command(aliases=["p"])
async def play(ctx, *args):
    """
    Play sounds
    
    Example: `?p สวัสดีครับ`
    """
    global voice_client
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
    sentence = ' '.join(args)
    if sentence not in sentence_mapper.keys():
        print("No this sentence in sentence_mapper")
        await ctx.reply("Not this sentence in list")
        return 
    filename = 'clips/' + sentence_mapper[sentence]
    if not path.exists(filename):
        print("No such file (" + sentence + ".mp3)")
        await ctx.reply(sentence + " does not exists.")
        return 
    global last 
    last = sentence_mapper[sentence ]
    user_channel = ctx.author.voice.channel

    if ctx.me.voice is None or ctx.me.voice.channel != user_channel:
        voice_client = await user_channel.connect() 
        
    voice_client.play(FFmpegPCMAudio(executable="ffmpeg/bin/ffmpeg.exe", source=filename))
    while voice_client.is_playing(): 
        await(asyncio.sleep(0.2))
        
@bot.command(aliases=["loop"])
async def play_loop(ctx, *args):
    """
    Play sounds
    
    Example: `?loop สวัสดีครับ`
    """
    global voice_client
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
    sentence = ' '.join(args)
    if sentence not in sentence_mapper.keys():
        print("No this sentence in sentence_mapper")
        await ctx.reply("Not this sentence in list")
        return 
    filename = 'clips/' + sentence_mapper[sentence]
    if not path.exists(filename):
        print("No such file (" + sentence + ".mp3)")
        await ctx.reply(sentence + " does not exists.")
        return 
    global last 
    last = sentence_mapper[sentence ]
    user_channel = ctx.author.voice.channel

    if ctx.me.voice is None or ctx.me.voice.channel != user_channel:
        voice_client = await user_channel.connect() 
        
    while True:
        voice_client.play(FFmpegPCMAudio(executable="ffmpeg/bin/ffmpeg.exe", source=filename))
        while voice_client.is_playing(): 
            await(asyncio.sleep(0.2))
    

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
    'ไอ้ {name} ไอ้หน้าหี ดับเบิ้ลหี สองหี สามหี',
    'หลอนละมึง ไอ {name}',
    'อย่าหลอนให้มาก ไอ้ {name}',
]

@bot.command(aliases=["b"])
async def cursing(ctx, *args):
    """
    Curse other people
    
    Example: `?b ทู`
    """
    global voice_client
    
    FILENAME = 'clips/curse.mp3'
    
    if len(args) == 0:
        print("No args, idiot.")
        
    name = args[0]
    if name == 'วิน':
        n = 5
    else:
        n = 1
    for i in range(n):
        tts = gTTS(text=choice(SENTENCES).format(name=name), lang='th')
        tts.save(FILENAME)
        user_channel = ctx.author.voice.channel

        if ctx.me.voice is None or ctx.me.voice.channel != user_channel:
            voice_client = await user_channel.connect() 
            
        voice_client.play(FFmpegPCMAudio(executable="ffmpeg/bin/ffmpeg.exe", source=FILENAME))
        while voice_client.is_playing(): 
            await(asyncio.sleep(0.2))
    

@bot.command(aliases=["r"])
async def random(ctx):
    r = choice(listdir("clips"))
    r = r[:-4]
    await play(ctx, r)
    
    
@bot.command(aliases=["dc"])
async def discon(ctx):
    global voice_client
    await voice_client.disconnect(force=True)


@bot.command(aliases=["re"])
async def replay(ctx):
    if last is None: 
        return 
    await play(ctx, last)


GREETINGS = [
    'สวัสดี {name}',
    'หวัดดี {name}',
    'ยินดีต้อนรับ {name}',
    '{name} เข้ามาแล้ว',
]

@bot.event
async def on_voice_state_update(member, before, after) :
    """
        This event could trigger when someone update their voice state
        voice state: None, self mute, self deafen, connect to channel ,etc.

        But for now we use it as "connect to some channel from None" greeting (change channel excluded)
    """
    global voice_client
    
    if before.channel is None and after.channel is not None and not member.bot:
        voice_client = await after.channel.connect() 
        await(asyncio.sleep(0.5))
        
        if uniform(0, 1) > 0.3:
            FILENAME = 'clips/welcome.mp3'
            tts = gTTS(text=choice(GREETINGS).format(name=member.display_name), lang='th')
            tts.save(FILENAME)
        else:
            FILENAME = 'clips/sà-wàt-dee kráp.mp3'
        
        voice_client.play(FFmpegPCMAudio(executable="ffmpeg/bin/ffmpeg.exe", source=FILENAME))
        while voice_client.is_playing(): 
            await(asyncio.sleep(0.5))
        try:
            if voice_client.channel is not None:
                await voice_client.disconnect() 
        except AttributeError:
            pass

bot.run(settings.DISCORD_TOKEN)
