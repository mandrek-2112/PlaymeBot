import spotipy
import spotipy.util as util
import random
from datetime import datetime
import os

from spotipy.oauth2 import SpotifyClientCredentials # to access authorised Spotify data

def makePlaylist(x, user):


	Client_id = os.environ.get("SpotifyClient_id")
	Client_secret = os.environ.get("SpotifyClient_secret")

	token = util.prompt_for_user_token(username="http://localhost:8888/callback", scope="playlist-modify-private, playlist-modify-public", client_id=Client_id,
	 client_secret=Client_secret, redirect_uri ="http://localhost:8888/callback")
	if token:
		sp = spotipy.Spotify(auth = token) # spotify object to access API
	else:
		print("Can't get token.")

	#x = "halsey"
	artist_name = x;
	 
	if '+' in x:  # remove all the "+" characters, breaks the search
		x = x.replace('+', '')
	else:
		x = x

	result0 = sp.search(q=x, type='artist')
	try:
		uri = result0['artists']['items'][0]['uri']
	except IndexError:
		uri = 'No URI'
		return "noartist"

	# testing purposes
	#print(uri)

	x = uri[15:] # get spotify id
	#print(x)

	i = 1
	related_artists = []
	related_artists.append(uri)

	RelatedArtSearch = sp.artist_related_artists(x)
	while i<11:
		try:
			relatedArtists = [RelatedArtSearch['artists'][i]['uri']]
		except IndexError:
			break;
		i = i+1
		related_artists.append(relatedArtists)

	# testing purposes
	#print(related_artists)
	# print(str(related_artists[0]).split(":")[2].split("\']")[0])

	i = 0
	related_songs = []

	while i<11:
		# if i==0:
		# 	related_songs.append(sp.artist_top_tracks(uri)['tracks'][i]['uri'])
		# else:
		RelatedSongs = sp.artist_top_tracks(str(related_artists[i]).split(":")[2].split("\']")[0])
		try:
			relatedSongs = [RelatedSongs['tracks'][random.randrange(0,6)]['uri']]
		except IndexError:
			break;
		i = i+1
		related_songs.append(relatedSongs)

	# testing purposes
	#print(related_songs)


	playlist = sp.user_playlist_create(user="f00z59vji8zqqy7pzp4h5qsx3", 
		name="Featuring {}: PlayMeBot for {} ({})".format(artist_name.title(),user, datetime.now().date()), public=True, 
		description='Auto suggested and created playlist by PlayMeBot.')
	playlist_id = str(playlist['id'])

	i=0
	while i<11:
		try:
			songs = sp.user_playlist_add_tracks(user="f00z59vji8zqqy7pzp4h5qsx3", playlist_id=playlist_id, tracks=related_songs[i])
			i = i+1
		except IndexError:
			break;

	#print("Hopefully done.")
#	print(playlist_id)
	return playlist_id

#makePlaylist("kodaline","test")