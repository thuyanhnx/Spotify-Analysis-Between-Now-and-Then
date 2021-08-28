#!/usr/bin/env python
# coding: utf-8

# Spotify API

# In order to read Spotify API, I need to apply for permissions & credentials through their Developer site. 
# I then used Python to scrape the Spotify API web (that I learned from multiple articles in "Towards Data Science" to extract all songs from our "On Repeat" playlist).

import json
import numpy as np
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_id = '' #insert your client id
client_secret = '' # insert your client secret id here

client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

playlist_id='' #playlist name
results = sp.playlist(playlist_id)


# Convert JSON to DataFrame

# create a list of song ids
ids=[]

for item in results['tracks']['items']:
        track = item['track']['id']
        ids.append(track)
        
song_meta={'id':[],'album':[], 'name':[], 
           'artist':[],'explicit':[],'popularity':[]}

for song_id in ids:
    # get song's meta data
    meta = sp.track(song_id)
    
    # song id
    song_meta['id'].append(song_id)

    # album name
    album=meta['album']['name']
    song_meta['album']+=[album]

    # song name
    song=meta['name']
    song_meta['name']+=[song]
    
    # artists name
    s = ', '
    artist=s.join([singer_name['name'] for singer_name in meta['artists']])
    song_meta['artist']+=[artist]
    
    # explicit: lyrics could be considered offensive or unsuitable for children
    explicit=meta['explicit']
    song_meta['explicit'].append(explicit)
    
    # song popularity
    popularity=meta['popularity']
    song_meta['popularity'].append(popularity)

song_meta_df=pd.DataFrame.from_dict(song_meta)

# check the song feature
features = sp.audio_features(song_meta['id'])

# change dictionary to dataframe
features_df=pd.DataFrame.from_dict(features)

# convert milliseconds to mins
# duration_ms: The duration of the track in milliseconds.
# 1 minute = 60 seconds = 60 × 1000 milliseconds = 60,000 ms
features_df['duration_ms']=features_df['duration_ms']/60000

# combine two dataframe
final_df=song_meta_df.merge(features_df)

# delete unnecessary columns
columns = ['uri','track_href','analysis_url']
final_df.drop(columns, inplace=True, axis=1)

# print final dataframe
print(final_df.head())

# We can conduct our analysis right after this step to get our data updated everytime we run this code again. 
# However, as I don't want to publish my account client id information, I will save the dataframe as .csv and then I will read them later in the analysis.

# Save as csv
final_df.to_csv('') 






