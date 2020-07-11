import tweepy
import logging
import time
import pickle
from findURI import makePlaylist

import os

def create_api():
    CONSUMER_KEY = os.environ.get("CONSUMER_KEY")
    CONSUMER_SECRET = os.environ.get("CONSUMER_SECRET")
    ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
    ACCESS_TOKEN_SECRET = os.environ.get("ACCESS_TOKEN_SECRET")

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    try:
        api.verify_credentials()
    except Exception as e:
        logging.error("Error creating API", exc_info=True)
        raise e
    logging.info("API created")
    return api

def check_mentions(api, since_id):
    logging.info("Retrieving mentions")
    print("Retrieving mentions")
    new_since_id = since_id
    for tweet in tweepy.Cursor(api.mentions_timeline, since_id=since_id).items():
        new_since_id = max(tweet.id, new_since_id)
        if tweet.in_reply_to_status_id is not None:
            continue
        req=tweet.text.lower()

        mentionPos=req.find("@playmebot")
        artist=req[mentionPos+10:]
        
        if len(artist)==0:
            st="Oops, we couldn't find the artist. Make sure you write the artist after the mention!"
        else:
            #Pass artist to spotify part, and it returns the spotify link 

            playlistID=makePlaylist(artist,tweet.user.name)
            print(playlistID)

            if playlistID == 'noartist':
                st="Oops, we couldn't find that artist, maybe try another one?"
            else:
                st="Hey "+ tweet.user.name+", hope you enjoy this playlist! open.spotify.com/playlist/"+str(playlistID)
 
            logging.info(f"Answering to {tweet.user.name}")
        api.update_status(status=st, in_reply_to_status_id=tweet.id, auto_populate_reply_metadata=True)
        with open('since_id.pk','wb') as f:
            pickle.dump(new_since_id, f)
    return new_since_id

def main():
    api = create_api()
    with open('since_id.pk','rb') as b:
        since_id=pickle.load(b)
    #print(since_id)
    while True:
        since_id = check_mentions(api, since_id)
        logging.info("Waiting...")
        print("Waiting...")
        time.sleep(60)


if __name__ == "__main__":
    main()
