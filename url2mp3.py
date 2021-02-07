import requests
import re 
from tqdm import tqdm  

raw_sounds = requests.get('https://prophet-button.netlify.app/')
sounds = re.findall(r'src=\"(.*\.mp3)\"', raw_sounds.text)

for sound in tqdm(sounds): 
    r = requests.get(f'https://prophet-button.netlify.app/sound/{sound}')
    with open(f'clips/{sound}', 'wb') as f:
        f.write(r.content)