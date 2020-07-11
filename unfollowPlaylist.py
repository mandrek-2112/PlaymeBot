import spotipy
import spotipy.util as util
import random
import datetime


from spotipy.oauth2 import SpotifyClientCredentials # to access authorised Spotify data

Client_id = "b10e8421036a4c54b38c5f0080b5a354"
Client_secret = "be52fd9dabd64bf295ed13039937eff8"
userID = "f00z59vji8zqqy7pzp4h5qsx3"

token = util.prompt_for_user_token(username=userID, scope="playlist-modify-private, playlist-modify-public", client_id=Client_id,
client_secret=Client_secret, redirect_uri ="http://localhost:8888/callback")
if token:
	sp = spotipy.Spotify(auth = token) # spotify object to access API
else:
	print("Can't get token.")

play_list = []
play_list_name = []
playlists = sp.user_playlists(userID)
for playlist in playlists['items']:
	if playlist['owner']['id'] == userID:
		print(playlist['name'])
		print(playlist['id'])
		play_list_name.append(playlist['name'])
		play_list.append(playlist['id'])

# print(datetime.datetime.now().date())
# 2020-07-09

# print(play_list)

# datetime.strptime(datetime_str, '%m/%d/%y %H:%M:%S')
# print(play_list_name[0].split("(")[1].split(")")[0])

i = 0
k=0
for plists in play_list_name:
	playlist_time = plists.split("(")[1].split(")")[0]
	if datetime.datetime.strptime(playlist_time, '%Y-%m-%d') < datetime.datetime.now(): # - datetime.timedelta(days=14):
		print(play_list_name[i])
		flag = sp.user_playlist_unfollow(userID, play_list[i])
		k = k+1
	i = i+1

print("{} playlist(s) were deleted".format(k))
print("The end, hopefully.")
