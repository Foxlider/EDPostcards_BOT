##INFORMATIONS
#
# Hello people ! I'm Foxlider. 
# About a year ago (about 2016) I created the #EDPostcards on Twitter. It started to gain quite a reputation. 
# But now I want people to be able to receive easily what people tweet on the hashtag whenever somebody tweet. 
# 
# And this lil BOT is born. THE END
#

# Installation : 
#   Just get the keys from twitter (CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET) 
#   Put them in a file called keyFile.txt in this EXACT order ! 
#   Create a 'dl' folder
#   Launch the BOT
#   TADAAAAA !
#
# But honestly, why would you run this bot if mine is already running ?

# Commands
#   shutdown    : To shutdown the BOT (quite obvious)
#   tweet [txt] : To send a tweet via the bot's console. txt is the message of the tweet.

# THE END


#Basic informations 
__program__ = "EDP Bot"
__version__ = "1.2a"

##Libraries imports
import tweepy
import wget
import time
import sys




##Variables setup
keysFile=open("keyFile.txt","r")
keys=keysFile.readlines()
consumer_key=keys[0].rstrip() # .rstrip() gets us rid off of \n
consumer_secret=keys[1]
keysFile.close()

CONSUMER_KEY = keys[0].rstrip()
CONSUMER_SECRET = keys[1].rstrip()
ACCESS_KEY = keys[2].rstrip()
ACCESS_SECRET = keys[3].rstrip()
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)
media_files = set()

##Functions and classes

def dl(media_files):
    i = 0
    dl_files = set()
    for url in media_files:
        i+=1
        print("downloading media "+str(i)+" : " +url)
        try:
            wget.download(url, out = "dl\img"+str(i)+".jpg")
        except:
            print('Unable to download file. Cancelling.')
        dl_files.add("dl\img"+str(i)+".jpg")
    return dl_files

class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        author = status.author.screen_name
        text = status.text
        if (not text.startswith("RT")):
            print("@"+author + " : \n"+text)
            #print(vars(status))
            media = status.entities.get('media', []) 
            if(len(media) > 0 ):
                print (str(len(media))+" media(s) detected")
                media_files.add(media[0]['media_url']) #IMPROVE IT !
                dl_files = dl(media_files)
                id = status.id_str
                api.retweet(id) # I can't seems to get more than 1 media per tweet and can't seems to send more than 1 media per tweet. So better RT
            else:
                print("No media detected.\n")
    
    def on_direct_message(self, status): #Can't handle direct message yet. Why ? Dunno.
        author = status.author.screen_name 
        text = status.text
        print(author + " : \n"+text)
        
    def on_error(self, status_code):
        print ("Error Code: " + str(status_code))
        if status_code == 420:
            return False
        else:
            return True

    def on_timeout(self):
        print('Timeout...')
        return True
## The bot itself  

print("BOT " + __program__ + " v" + __version__ + " started. \nConnection...")

try:
    api.update_profile(location="Sol")
    me = api.me()
    print("Logged in as @"+ me.screen_name +" !")
    #print (vars(me))
except tweepy.TweepError:
    print ("Could not authenticate you. \nExiting the program.")
    exit()
print("____[ INFORMATIONS ]____")
print("@"+me.screen_name)
print(str(me.followers_count)+" followers : ")
for follower in me.followers():
   print(" -"+follower.screen_name)
   follower.follow()

myStreamListener = MyStreamListener()
try:
    if myStream.running:
        print ("Stream already running.")
        myStream.disconnect()
    else:
        print("Stream not running. Starting Stream...")
except:
    print("Stream not Detected. Starting Stream...")

myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
myStream.filter(track=['EDPostcards'], async=True)

if myStream.running:
    print ("Stream running.")
else:
    print("Stream startup failed")
shutdown = False
time.sleep(5)
while not shutdown:
    ans = input("Command ? : \n>>>")
    if (ans == "shutdown"):
        print("Logging off...")
        shutdown = True
        api.update_profile(location="In a debris field")
        myStream.disconnect()
        print("Shuting down...")
        quit()
    if (ans.startswith("tweet ")):
        text = ans.strip("tweet ")
        #print(text)
        api.update_status(status=text)
    time.sleep(1)



