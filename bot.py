import sys 
sys.path.append('..')
from discord.ext import commands
from discord import FFmpegPCMAudio, Embed
from discord import utils

import os 
import json 
import asyncio
import settings 
import requests

from random import choice, uniform
from os import path
from os import listdir
from gtts import gTTS

import requests
import re 
from tqdm import tqdm  

last = None

def create_sentence_mapper():
    os.makedirs('clips', exist_ok=True)

    raw_sounds = requests.get('https://prophet-button.netlify.app/')
    extracted_data = re.findall(r'src=\"(.*\.mp3)\".*\">([^\"<]*)<', raw_sounds.text)

    sentence_mapper = dict() 
    for (filename, sentence) in tqdm(extracted_data):
        sentence_mapper[' '.join(sentence.split()).strip()] = filename
        r = requests.get(f'https://prophet-button.netlify.app/sound/{filename}')
        with open(f'clips/{filename}', 'wb') as f:
            f.write(r.content)

    with open('sentence_mapper.json', 'w') as f:
        json.dump(sentence_mapper, f)

def get_sentence_mapper():
    global sentence_mapper
    try:
        with open('sentence_mapper.json', 'r') as f:
            sentence_mapper = json.load(f)
    except FileNotFoundError:
        create_sentence_mapper()
        get_sentence_mapper()

get_sentence_mapper()

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
        
    voice_client.play(FFmpegPCMAudio(source=filename))
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
        voice_client.play(FFmpegPCMAudio(source=filename))
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
    for i in range(1):
        tts = gTTS(text=choice(SENTENCES).format(name=name), lang='th')
        tts.save(FILENAME)
        user_channel = ctx.author.voice.channel

        if ctx.me.voice is None or ctx.me.voice.channel != user_channel:
            voice_client = await user_channel.connect() 
            
        voice_client.play(FFmpegPCMAudio(source=FILENAME))
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
    'จ๊ะเอ๋ {name}',
    'ฮู่เล่ {name}',
    'ทาดา {name}',
    'ฮัลโหล {name}',
    'ยาเลยาเล {name}',
    'อย่าหลอน {name}',
    'ออกไปเลย {name}',
    'ใครเข้ามาหน่ะ อ๋อ {name}',
    '{name} เข้ามาทำไม',
    '{name} ออกไปเดี๋ยวนี้เลยนะ',
    '{name} ออกไปไกลๆเลย',
    '{name} บอก กามู',
    'กูตื่นแล้ว ไอ้ {name} ตื่นรึยัง',
    'งานการไม่ทำหรอวะ ไอ้ {name}',
    '{name} อยากเข้าก็เข้า ทำตัวเป็นลุงตู่ไปได้'
]

BYES = [
    'ใครจะอยู่ก็อยู่ แต่ {name} ไม่อยู่แล้ว',
    '{name} ออกไปทำเหี้ยไร',
    '{name} ออกไปแล้ว แต่ลุงตู่ยังไม่ออก',
    '{name} ไปละ ด่ามันได้',
    'จะไปไหนก็ไป {name}',
    'กูถีบไอ่ {name} ออกไปแล้ว',
    'ลาก่อย {name}',
    'ไอ่ {name} มันหนีไปกรอกน้ำให้แม่',
    '{name} บอกว่าไกปู',
    '{name} กับเพื่อนกับฝูงไม่เคยจะอยู่',
    'ใครออกไปน้า อ๋อ {name}',
    'ไอ่เอ๋อ {name} นี่ออกไปอีกละ',
    'ว้ายๆ ไอ้ {name} ไปนอนแล้ว',
    '{name} บอกกูไปขี้แปป',
    '{name} หนีเพื่อนไปดูหมอลำอีกแล้ว'
]

BYES_FROM_FILE = [
    'preview_4.mp3',
    'disconnect.mp3',
    'cp-sound-get-out.mp3',
]

GREETINGS_FROM_FILE = [
    'cp-sound-really.mp3',
    'pornhub-community-intro.mp3',
    'hello_motherfrucker.mp3',
    '.mp3_5M3Zb4t',
    'among.mp3',
    'kids_cheering.mp3',
    'dry-fart.mp3',
]

def download_file_from_myinstants(filename):
    url = f'https://www.myinstants.com/media/sounds/{filename}'
    r = requests.get(url)
    with open(f'clips/{filename}', 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
    return None

for name in GREETINGS_FROM_FILE:
    download_file_from_myinstants(name)

for name in BYES_FROM_FILE:
    download_file_from_myinstants(name)

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
        
        message = choice(GREETINGS + GREETINGS_FROM_FILE)
        
        if message in GREETINGS:
            FILENAME = 'clips/welcome.mp3'
            tts = gTTS(text=message.format(name=member.display_name), lang='th')
            tts.save(FILENAME)
        else:
            FILENAME = f'clips/{message}'
            
        voice_client.play(FFmpegPCMAudio(source=FILENAME))
        while voice_client.is_playing(): 
            await(asyncio.sleep(0.5))
        try:
            if voice_client.channel is not None:
                await voice_client.disconnect() 
        except AttributeError:
            pass
    if before.channel is not None and after.channel is None and not member.bot :
        voice_client = await before.channel.connect() 
        await(asyncio.sleep(0.5))
        message = choice(BYES + BYES_FROM_FILE)

        if message in BYES:
            FILENAME = 'clips/bye.mp3'
            tts = gTTS(text=message.format(name=member.display_name), lang='th')
            tts.save(FILENAME)
        else :
            FILENAME = f'clips/{message}'
        
        voice_client.play(FFmpegPCMAudio(source=FILENAME))
        while voice_client.is_playing(): 
            await(asyncio.sleep(0.5))
        try:
            if voice_client.channel is not None:
                await voice_client.disconnect() 
        except AttributeError:
            pass

bot.run(settings.DISCORD_TOKEN)
