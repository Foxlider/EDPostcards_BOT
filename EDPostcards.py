##INFORMATIONS
#
# Hello people ! I'm Foxlider.
#
# About a year ago (about 2016) I created the #EDPostcards on Twitter.
# It started to gain quite a reputation.
# But now I want people to be able to receive easily what people tweet on the hashtag whenever somebody tweet.
# 
# And this lil BOT is born. 
# THE END
#

# Installation :
#   Just get the keys from twitter (CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET)
#   Put them in a file called keyFile.txt in this EXACT order !
#   Launch the BOT
#   TADAAAAA !
#
# But honestly, why would you run this bot if mine is already running ?

# Commands
#   shutdown    : To shutdown the BOT (quite obvious)
#   reboot      : To reboot the BOT
#   restart     : To reboot the BOT
#   tweet [txt] : To send a tweet via the bot's console. txt is the message of the tweet.

# THE END

#Basic informations
__program__ = "EDPostcards Bot"
__version__ = "2.1a"

##Libraries imports
import datetime
import sys
try:
    assert sys.version_info >= (3, 4)
    import tweepy
    import wget
    import json
    import ftplib
except ImportError as error:
    print(__program__+"needs tweepy, wget, ftplib and json to work properly. Please install them using pip install <module>. \n" + str(error))
    sys.exit()
except AssertionError:
    print(__program__+'needs python 3.4 or greater to work properly. Please see the installation guide for your Operating System.')
    sys.exit()
import time
import random
import os




##Variables setup
if "--verbose" in sys.argv: #Sys Args
    Verbose = True
else:
    Verbose = False

#Twitter AUTH
try:
    keysFile = open("data/keyFile.txt", "r")
except IOError  as error:
    print(str(error) + "\nkeyFile doesn't exists. What have you done ? Nooooo ! *couic*")
    quit()
keys = keysFile.readlines()
keysFile.close()
CONSUMER_KEY = keys[0].rstrip()
CONSUMER_SECRET = keys[1].rstrip()
ACCESS_KEY = keys[2].rstrip()
ACCESS_SECRET = keys[3].rstrip()
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)


#FTP AUTH
try:
    keysFile = open("data/ftpFile.txt", "r")
except IOError  as error:
    print(str(error) + "\nkeyFile doesn't exists. What have you done ? Nooooo ! *couic*")
    quit()
keys = keysFile.readlines()
keysFile.close()
ADDR = keys[0].rstrip()
IDENT = keys[1].rstrip()
PWD = keys[2].rstrip()

bigBoss = ["Foxlidev", "FoxliderAtom", "ED_Postcards"] #Put here your Twitter name to be an admin

#Add texts here to increase the BOT's vocabulary and allow it to say more things !
quoteText = dict(quote1='They told me to quote this and I  refused. But those pics are great, so...',
                 quote2='OMG I love those ! This guy is a genius !',
                 quote3='My program is telling me that this stuff is awesome and that I must quote it.',
                 quote4='Oh my ! You really should watch this ! I am clearly not overreacting ! ',
                 quote5="This images are splendid. I'm happy to share them with you.",
                 quote6="I may be a robot, but I know how to appreciate real ART !",
                 quote7="I must... Resist... To... QUOTE ! NOOOOOOO ! ",
                 quote8='You want some pics ? You love those pics... Take those pics ! ',
                 quote9='His work is awesome. Check this out ! ',
                 quote10='Wow ! I liked this game but now i really love it ! ',
                 quote11='Is that some Elite Dangerous screenshots ? Of course it is !',
                 quote12="You know you want these screenshots. You want them ! ",
                 quote13="\"From space, with love\" -ED_Postcards",
                 quote14="Fly safe, CMDRs !",
                 quote15="These are incredible ! Check this out !",
                 quote16="I don't know what to say. It's just wonderful ! ",
                 quote17="This is it. I am in love.",
                 quote18="I have one word only in mind : Incredible.",
                 quote19="I have one word only in mind : Splendid.",
                 quote20="This game offers some pretty postcards for sure !",
                 quote21="I could spend hours of my time looking at this.",
                 quote22="Too bad I don't have any eyes to enjoy this.",
                 quote23="My core is heating just by looking at these pictures.",
                 quote24="I'd love to jump into one of those ships and enjoy the view.",
                 quote25="I'll force my developper to log me in his ship.",
                 quote50="I am running out of ideas for texts. So... Here, take this.")

#The filter
Hashtag = "EDPostcards"



datadir = os.path.dirname("./data/")
if not os.path.exists(datadir):
    os.makedirs(datadir)
if not os.path.exists("./dl/"):
    os.makedirs("./dl")


##  MAIN FUNCTIONS
def verbose(text):
    """
        Function used to log text in a file and printing it in the console.
        Replacing usual print()
        params :
            text    : text to print
    """
    if Verbose:
        fold = os.path.dirname("./logs/verbose/")
        if not os.path.exists(fold):
            os.makedirs(fold)
        today = datetime.datetime.now()
        logsFile = open(fold +"/"+ str(today.year) + "-" + str(today.month) + "-" + str(today.day) + ".txt", "a")
        log = "[" + str(today.hour) + ":" + str(today.minute) + ":" + str(today.second) + "] " + text + "\n"
        logsFile.write(log)
        print(log, end='')
        logsFile.close()

def logStart():
    """
        Function used to log in a file at startup
    """
    fold = os.path.dirname("./logs/")
    if not os.path.exists(fold):
        os.makedirs(fold)
    today = datetime.datetime.now()
    logsFile = open("./logs/startup.txt", "a")
    log = "[" + str(today) + "] : Bot " + __program__ + " v" + __version__ + " logged in\n"
    logsFile.write(log)
    print(log, end='')

def logText(text):
    """
        Function used to log text in a file and printing it in the console.
        Replacing usual print()
        params :
            text    : text to print
    """
    fold = os.path.dirname("./logs/console/")
    if not os.path.exists(fold):
        os.makedirs(fold)
    today = datetime.datetime.now()
    logsFile = open(fold +"/"+ str(today.year) + "-" + str(today.month) + "-" + str(today.day) + ".txt", "a")
    log = "[" + str(today.hour) + ":" + str(today.minute) + ":" + str(today.second) + "] " + text + "\n"
    logsFile.write(log)
    print(log, end='')
    logsFile.close()

def logError(errnum=0, errtext=""):
    """
        Function used to print errors in a file
        params:
            errnum      : code of the error between 100 and 999
            errtext     : details of the error
    """
    fold = os.path.dirname("./logs/errorLogs/")
    if not os.path.exists(fold):
        os.makedirs(fold)
    today = datetime.datetime.now()
    logsFile = open(fold +"/"+ str(today.year) + "-" + str(today.month) + "-" + str(today.day) + ".txt", "a")
    log = "[" + str(today.hour) + ":" + str(today.minute) + ":" + str(today.second) + "] 0x0" + str(errnum) + " : " + errtext + "\n"
    logsFile.write(log)
    print(log, end='')
    logsFile.close()
    frestart() #Here till I find a way to prevent disconnects

def dump(obj, nested_level=0, output=sys.stdout):
    """
        Function used for debugging
        It writes down in the console every detail of the object sent.
        params :
            obj          : object analysed
            nested_level : Number of tabs
            output       : Where to write
    """
    spacing = '   '
    if type(obj) == dict:
        logText('%s{' % ((nested_level) * spacing))
        for k, v in obj.items():
            if hasattr(v, '__iter__'):
                logText('%s%s:' %((nested_level + 1)* spacing, k))
                dump(v, nested_level + 1, output)
            else:
                logText('%s%s: %s' %((nested_level + 1)* spacing, k, v))
        logText('%s}' %(nested_level * spacing))
    elif type(obj) == list:
        logText('%s[' %((nested_level)* spacing))
        for v in obj:
            if hasattr(v, '__iter__'):
                dump(v, nested_level + 1, output)
            else:
                logText('%s%s' % ((nested_level + 1) * spacing, v))
        logText('%s]' % ((nested_level) * spacing))
    else:
        logText('%s%s' % (nested_level * spacing, obj))

def dl(media_files, sender):
    """
        This function is used to download the status medias if there is any.
        params :
            media_files : list of the urls of each medias from the status
            sender      : screen_name of the status sender
        return a list of the files urls
    """
    i = 0
    folder = "dl/"+sender+"/"
    if not os.path.exists(folder):
        os.makedirs(folder)
    today = datetime.datetime.now()

    dl_files = set()
    for url in media_files:
        i += 1
        name = str(today.day) + "-" + str(today.month) + "_" + str(today.hour) + "h" + str(today.minute) + "_" + str(i) + '.jpg'
        logText("downloading media "+str(i)+" : " +url + " to " + folder + name)
        try:
            wget.download(url, out=folder+name)
            dl_files.add(name)
        except Exception as error:
            logText(str(error)+"\nUnable to download file. Cancelling.")
            logError(156, str(error)+"\nUnable to download file.")
        except:
            logText("Oops I fucked up... You didn't wanted this anyway.")
            logError(157, "Nomething bad happened...")
    media_files = set()
    return dl_files, folder

def ftpSend(dlFiles, fold):
    """
        This function is used to send filed to the ftp server
        params :
            dlFiles : List of files to send
            fold    : Folder
    """
    try:
        session = ftplib.FTP(ADDR, IDENT, PWD)
        session.cwd('/dev/dls/wp-content/uploads/EDPostcards')
        #print('\n    =EDPostcards Folder')
        #session.retrlines('LIST')
        #print(str(session.nlst()) + '\n' + str(fold[3:-1]))
        if fold[3:-1] not in session.nlst():
            print('New user detected. Creating user folder')
            session.mkd(fold[3:])
        session.cwd(fold[3:])
        for fName in dlFiles:
            #fName = fold.split('/')[-1]
            openFile = open(fold+fName, 'rb')
            code = session.storbinary('STOR ' + fName, openFile)
            print('File ' + fName + ' sent to ' + fold[3:] + '\n' + str(code))
            openFile.close()
        session.quit()
    except Exception as error:
        logText(str(error))

def fshutdown():
    """
        This function is supposed to shut down the bot by disconnecting each stream.
    """
    logText("Logging off...")
    api.update_profile(location="In a debris field")
    mainStream.disconnect()
    cmdStream.disconnect()
    logText("Shuting down...")
    os.system("pkill EDPostcards")
    sys.exit()
    logText("Impossible to Shutdown")

def frestart():
    """
        this function is supposed to shutdown then restart the bot
    """
    logText("Restarting...")
    try: #As I might be disconnected...
        api.update_profile(location="In a debris field")
        mainStream.disconnect()
        cmdStream.disconnect()
    except:
        pass
    os.system("./../EDPostcards.sh")

##  CHECK FUNCTIONS
def IsStatus(status):
    """
    Function to test if the given object is a status
        :param status:
    """
    if "in_reply_to_status_id" in status and not "event" in status:
        #logText("Is Status")
        return True
    #logText("Is Not Status")
    return False

def IsRetweet(status):
    """
    Function to test if the given object is a retweet
        :param status:
    """
    if IsStatus(status):
        if getStatusText(status).startswith("RT "):
            #logText("Is RT")
            return True
    #logText("Is Not RT")
    return False

def IsDirectMessage(status):
    """
    Function to test if the given object is a direct message
        :param status:
    """
    if "direct_message" in status:
        #logText("Is DM")
        return True
    #logText("Is Not DM")
    return False

def HaveSent(user, status):
    """
    Function to test if the given user have sent the status
        :param user:
        :param status:
    """
    if IsStatus(status):
        if user.id == status["user"]["id"]:
            #logText("Is Sender")
            return True
    if IsDirectMessage(status):
        if user.id == status["direct_message"]["sender"]["id"]:
            #logText("Is Sender")
            return True
    #logText("Is Not Sender")
    return False

def IsInStatus(query, status):
    """
    Function to test if the given text is in the status
        :param query:
        :param status:
    """
    if query.lower() in getStatusText(status).lower():
        #logText("Is In Status")
        return True
    return False

def HaveHashTag(status, hashtag):
    """
    Function to test if the given hashtag is in the status
        :param status:
        :param hashtag:
    """
    if "#"+hashtag.lower() in getStatusText(status).lower():
        #logText("Have Hashtag")
        return True
    #logText("Don't Have Hashtag")
    return False

def HaveImages(status):
    """
    Function to test if the given status have medias
        :param status:
    """
    if "extended_tweet" in status:
        if "extended_entities" in status["extended_tweet"]:
            if "media" in status["extended_tweet"]["extended_entities"]:
                #logText("Media in extended tweet")
                return True
        elif "media" in status["entities"]:
            #logText("Media in Entities")
            return True
    else:
        if "extended_entities" in status:
            if "media" in status["extended_entities"]:
                #logText("Media in Extended entities")
                return True
        else:
            if "media" in status["entities"]:
                #logText("Media in simple Entities")
                return True
    #logText("No Media")
    return False

def IsMentionned(user, status):
    """
    Function to test if the given user is mentionned in the status
        :param user:
        :param status:
    """
    for ment in status["entities"]["user_mentions"]:
        if user.id == ment["id"]:
            #logText("Is Mentionned")
            return True
    #logText("Is Not Mentionned")
    return False

## TWITTER FUNCTIONS

def getStatusText(status):
    """
    Function to the status text
        :param status:
    """
    if "extended_tweet" in status:
        #verbose("Extended tweet")
        return status["extended_tweet"]["full_text"]
    #verbose("Standard tweet")
    return status["text"]

def dataHandler(data):
    """
    Function to handle data like tweets or direct messages
        :param data:
    """
    if not "friends" in data:
        if IsStatus(data) and not IsRetweet(data) and not HaveSent(me, data) and (IsMentionned(me, data) or HaveHashTag(data, Hashtag)): #and HaveImages(data)
            handleImageStatus(data)
        elif IsDirectMessage(data) and not HaveSent(me, data):
            handleCommand(data)

def handleImageStatus(status):
    """
    Function to handle a status
        :param status:
    """
    if HaveHashTag(status, Hashtag):
        logText("Hashtag Status !")
    elif IsMentionned(me, status):
        logText("Mentionned Status !")
    else:
        logText("WAT")
    if HaveImages(status):
        quoteStatus(status["id"])

def handleCommand(command):
    """
    Function to handle commands
        :param status:
    """
    #logText("This is a command !\n" + command["direct_message"]["text"])
    cmd = command["direct_message"]["text"] #Cuz I'm lazy
    if cmd.lower() == "shutdown":
        logText("Command received. Shutting Down...")
        fshutdown()
    elif cmd.lower() == "restart" or cmd.lower() == "reboot":
        frestart()
    else:
        if cmd.lower().startswith("tweet "):
            text = cmd[6:]
            try:
                api.update_status(status=text)
            except tweepy.TweepError as error:
                logError(error.args[0][0]['code'], error.args[0][0]['message'])
        elif cmd.lower().startswith('quote '):
            statusId = cmd[6:].split(' ')[0]
            quoteStatus(statusId)
        elif cmd.lower().startswith("foo "):
            text = cmd[4:]
            logText("bar : " + text)

def quoteStatus(statusId):
    """
    Function to quote the given status
        :param statusId:
    """
    decoded = api.get_status(statusId)
    sender = decoded.user.name
    sendertag = decoded.user.screen_name
    text = decoded.text
    media = set()
    media_files = set()
    if hasattr(decoded, "extended_tweet"):
        if hasattr(decoded.extended_tweet, "extended_entities"):
            media = decoded.extended_tweet.extended_entities["media"]
        elif hasattr(decoded.entities, "media"):
            logText("Media in Entities")
            media = decoded.entities["media"]
    else:
        if hasattr(decoded, "extended_entities"):
            media = decoded.extended_entities["media"]
        elif hasattr(decoded.entities, "media"):
            media = decoded.entities["media"]

    logText("Status n°"+str(statusId)+" by @"+ sender + "\n\""+text+"\" ("+str(len(media)) + " media files)")
    if len(media) >= 1:                                                 #Did we got some medias ?
        for i in media:
            media_files.add(i["media_url_https"])                       #Add medias to var
        dlFiles, folder = dl(media_files, sendertag)                             #Get those medias in your files
        ftpSend(dlFiles, folder)
        qcode, qtext = random.choice(list(quoteText.items()))           #Get one of the quote answers
        api.update_status(status=qtext+" https://twitter.com/"+sendertag+"/status/"+str(statusId))
    return False

class mainStreamListener(tweepy.StreamListener): #MAIN STREAM TO HANDLE HASHTAG TREATMENT
    """
    Main Stream Class
        :param tweepy.StreamListener:
    """
    def on_data(self, status):
        #dump(self)
        logText("mainStream called")
        decoded = json.loads(status)
        dataHandler(decoded)

    def on_error(self, status_code):
        logText("Error Code: " + str(status_code))
        logError(status_code, "Twitter API error. Refer to dev.twitter.com for more informations")
        if status_code == 420:
            frestart()
            return False
        frestart()
        return True

    def on_timeout(self):
        logError(105, 'Timeout...')
        frestart()
        return True

class cmdStreamListener(tweepy.StreamListener): #THIS ONE IS USED FOR COMMANDS HANDLING ONLY
    """
    Command Stream Class
        :param tweepy.StreamListener:
    """
    def on_data(self, status):
        #logText("I heard something...")
        logText("cmdStream called")
        decoded = json.loads(status)
        dataHandler(decoded)
    def on_error(self, status_code):
        logText("Error Code: " + str(status_code))
        logError(status_code, "Twitter API error. Refer to dev.twitter.com for more informations")
        if status_code == 420:
            frestart()
            return False
        frestart()
        return True
    def on_timeout(self):
        logError(105, 'Timeout...')
        frestart()
        return True

## The bot itself

logText("BOT " + __program__ + " v" + __version__ + " started. \nConnection...")
logStart()
verbose("BOT " + __program__ + " v" + __version__ + " started. \nVerbose activated")
try:    #Main loop

    try:        #API Settings
        api.update_profile(location="Sol")
        api.timeout = 240
        api.retry_count = 3
        api.wait_on_rate_limit = True
        api.wait_on_rate_limit_notify = True
        me = api.me()
        logText("Logged in as @"+ me.screen_name +" !")
        #print (vars(me))
    except tweepy.TweepError:
        logText("Could not authenticate you. \nExiting the program.")
        logError(420, str(tweepy.TweepError)+" Could not authenticate you.")
        exit()
    logText("____[ INFORMATIONS ]____")
    logText("@"+me.screen_name)
    logText(str(me.followers_count)+" followers : ")
    for follower in me.followers():     #Follower handler
        if not follower.following:
            try:
                logText(" -"+follower.screen_name)
                follower.follow()
            except tweepy.TweepError:
                logError(421, str(tweepy.TweepError)+" Follow error.")
    #for follower in api.friends_ids(me.id):
    #   if (not api.lookup_friendships(me.id)):
    #        try:
    #            logText(" -"+follower.screen_name)
    #            logText("I should unfollow this idiot.")
    #            #follower.unfollow()
    #        except tweepy.TweepError:
    #            logError(421, str(tweepy.TweepError)+" Unfollow error.")

    try:                                                #Starting streams
        if mainStream.running or cmdStream:
            logText("Stream already running.")
            #mainStream.disconnect()
            cmdStream.disconnect()
        else:
            logText("Stream not running. Starting Stream...")
    except:
        logText("Stream not Detected. Starting Stream...")

    #mainStream = tweepy.Stream(auth=api.auth, listener=mainStreamListener())
    time.sleep(3) #So twitter calms down a little
    cmdStream = tweepy.Stream(auth=api.auth, listener=cmdStreamListener())

    #mainStream.filter(track=[Hashtag], async=True)
    cmdStream.userstream(async=True)
    shutdown = False

    #if mainStream.running:
    #    logText("MainStream running.")
    #else:
    #    logText("MainStream startup failed")
    #    fshutdown()
    if cmdStream.running:
        logText("CMDStream running.")
    else:
        logText("CMDStream startup failed")
        fshutdown()
    time.sleep(2)
    


except tweepy.TweepError:
    logError(880, str(error))
    frestart()
except Exception as error:
    logError(990, str(error))
    frestart()
