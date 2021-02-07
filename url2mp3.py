import requests
import re 
import os 
from tqdm import tqdm  
import json 

os.makedirs('clips', exist_ok=True)

raw_sounds = requests.get('https://prophet-button.netlify.app/')
extracted_data = re.findall(r'src=\"(.*\.mp3)\".*\">([^\"<]*)<', raw_sounds.text)

sentence_mapper = dict() 
for (filename, sentence) in tqdm(extracted_data):
    sentence_mapper[sentence.strip()] = filename
    r = requests.get(f'https://prophet-button.netlify.app/sound/{filename}')
    with open(f'clips/{filename}', 'wb') as f:
        f.write(r.content)

with open('sentence_mapper.json', 'w') as f:
    json.dump(sentence_mapper, f)