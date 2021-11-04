import requests 
import pandas as pd 
import json 
import matplotlib.pyplot as plt
import time

l2=[]
l=list(range(3000))

def retrieve_data(l):
    for el in l:
        url='https://api.jikan.moe/v3/anime/'+str(el)+'/'
        req=requests.get(url).json()
        time.sleep(4)
        if str(req['status'])=='404':
            el+=1
        else:
            l2.append(req)
            el+=1
    return l2 
retrieve_data(l)

df = pd.DataFrame(columns=['anime_name', 'anime_id','type','episodes','score','rank','popularity','scored_by','likes','aired_from','aired_to','duration','Storyline'])
def create_dataframe(l2,df):
    i = 0
    for el in l2:
        try :
            anime_name=l2[i]['title']
        except KeyError:
            anime_name=None
        try:
            anime_id=l2[i]['mal_id']
        except KeyError:
            anime_id=None  
        try:
            typology=l2[i]['type']
        except:
            typology=None
        try :
            n_episodes=l2[i]['episodes']
        except KeyError:
            n_episodes=None
        try:
            score=l2[i]['score']
        except KeyError:
            score=None
        try :
            rank=l2[i]['rank']
        except KeyError:
            rank=None
        try:
            popularity=l2[i]['popularity']
        except KeyError:
            popularity=None
        try:
            scored_by=l2[i]['scored_by']
        except KeyError:
            scored_by=None
        try:
            likes=l2[i]['favorites']
        except KeyError:
            likes=None
        try :
            duration=l2[i]['duration']
        except KeyError:
            duration=None
        try:
            start_airing_time=l2[i]['aired']['from']
        except KeyError:
            start_airing_time=None
        try :
            end_airing_time=l2[i]['aired']['to']
        except KeyError:
            end_airing_time=None
        try:
            Storyline=l2[i]['synopsis']
        except KeyError:
            Storyline=None
      
        i+=1
        df = df.append({'anime_name': anime_name, 'anime_id':anime_id, 'episodes':n_episodes, 'type':typology, 'score':score,'rank':rank,'popularity':popularity,'scored_by':scored_by,'likes':likes,'duration':duration,'aired_from':start_airing_time,'aired_to':end_airing_time,'Storyline':Storyline}, ignore_index=True)
    return df 
df=create_dataframe(l2,df)

