import requests
import re
import pandas as pd
from bs4 import BeautifulSoup

url_list = ["https://animalcrossing.fandom.com/wiki/Guide:Cranky_dialogues_(New_Leaf)", "https://animalcrossing.fandom.com/wiki/Guide:Peppy_dialogues_(New_Leaf)",
"https://animalcrossing.fandom.com/wiki/Guide:Player_dialogues","https://animalcrossing.fandom.com/wiki/Guide:Normal_dialogues_(New_Leaf)",
"https://animalcrossing.fandom.com/wiki/Guide:Lazy_dialogues_(New_Leaf)", "https://animalcrossing.fandom.com/wiki/Guide:Sisterly_dialogues_(New_Leaf)",
"https://animalcrossing.fandom.com/wiki/Guide:Jock_dialogues_(New_Leaf)", "https://animalcrossing.fandom.com/wiki/Guide:Smug_dialogues_(New_Leaf)",
"https://animalcrossing.fandom.com/wiki/Guide:Snooty_dialogues_(New_Leaf)"]
label_list = ["cranky","peppy","player","normal","lazy","uchi","jock","smug","snooty"]
#the format of these pages is slightly different, so they are their own list
p_urls = ["https://animalcrossing.fandom.com/wiki/Guide:Isabelle_dialogues","https://animalcrossing.fandom.com/wiki/Guide:Resetti_dialogues_(Animal_Crossing)",
"https://animalcrossing.fandom.com/wiki/Franklin_Dialogue_(GCN)", "https://animalcrossing.fandom.com/wiki/Jingle_Dialogue_(GCN)"]
p_labels = ["isabelle","resetti","franklin","jingle"]

dialogue = []
labels = []
pattern = re.compile("\"([\S+\s]+)\"")

for j in range(len(url_list)):
    page = requests.get(url_list[j])
    soup = BeautifulSoup(page.content, 'html.parser')
    li = soup.find_all('li')
    for item in li:
        for i in item.children:
            if i.string != None:
                text = i.string
                #use regex to clean up the string
                clean = pattern.match(text)
                if clean != None:
                    dialogue.append(clean.group(1))
                    labels.append(label_list[j])
    
for i in range(len(p_urls)):
    page = requests.get(p_urls[i])
    soup = BeautifulSoup(page.content, 'html.parser')
    p = soup.find_all('p')
    for paragraph in p:
        if paragraph.string != None:
            text = paragraph.string
            #use regex to clean up the string
            clean = pattern.match(text)
            if clean != None:
                dialogue.append(clean.group(1))
                labels.append(p_labels[i])
print("Dialogue has been scraped!")

df_data = {'dialogue':dialogue, 'labels':labels}
dialogue_df = pd.DataFrame(df_data)
dialogue_df.to_csv('dialogue.csv', index=False)
print("Dialogue has been saved!")