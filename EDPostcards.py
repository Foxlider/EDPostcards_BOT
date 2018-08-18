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
__version__ = "2.2b"

##Libraries imports
import datetime
import sys
import configparser
try:
    assert sys.version_info >= (3, 4)
    import tweepy
    import wget
    import json
except ImportError as error:
    print(f"{__program__} needs tweepy, wget, ftplib and json to work properly. Please install them using pip install <module>. \n{error}")
    sys.exit()
except AssertionError:
    print(f"{__program__} needs python 3.4 or greater to work properly. Please see the installation guide for your Operating System.")
    sys.exit()
import time
import random
import os

filepath = os.path.dirname(os.path.realpath(__file__))


##Variables setup
if "--verbose" in sys.argv: #Sys Args
    Verbose = True
else:
    Verbose = False

#Config file
config = configparser.ConfigParser()
config.optionxform = str
try:
    config.read(f'{filepath}/data/config.cfg')
    bestUsers = config['BestUsers']
except Exception as error:
    print(f" -- ERROR : Config file not detected. Have you launched the installer first ?\n{error}")
    quit()



#Twitter AUTH
CONSUMER_KEY = config["Keys"]["CONSUMER_KEY"]
CONSUMER_SECRET = config["Keys"]["CONSUMER_SECRET"]
ACCESS_KEY = config["Keys"]["ACCESS_KEY"]
ACCESS_SECRET = config["Keys"]["ACCESS_SECRET"]
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)


#FTP AUTH
#try:
#    keysFile = open("data/ftpFile.txt", "r")
#except IOError  as error:
#    print(f"{error}\nkeyFile doesn't exists. What have you done ? Nooooo ! *couic*")
#    quit()
#keys = keysFile.readlines()
#keysFile.close()
#ADDR = keys[0].rstrip()
#IDENT = keys[1].rstrip()
#PWD = keys[2].rstrip()

bigBoss = ["Foxlidev", "FoxliderAtom", "ED_Postcards"] #Put here your Twitter name to be an admin

#Add texts here to increase the BOT's vocabulary and allow it to say more things !
quoteText = dict(quote1='Oh man ! I neede to quote this pictures ! ',
                 quote2='I love those ! This guy is a genius !',
                 quote3='My program is telling me that this stuff is awesome and that I must quote it.',
                 quote4='Oh my ! You really should watch this ! I am clearly not overreacting ! ',
                 quote5="I'm happy to share these images with you.",
                 quote6="I may be a robot, but I know how to appreciate real ART !",
                 quote7="Here you go ! Fresh pictures out of my drives ! ",
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
                 quote22="Too bad I don't have any eyes to enjoy this as much as you can.",
                 quote23="My core is heating just by looking at these pictures.",
                 quote24="I'd love to jump into one of those ships and enjoy the view.",
                 quote25="I'll force my developper to log me in his ship.",
                 quote26="When i received these images, my cycles per second just stopped for a second !",
                 quote27="Whoah ! My core temp just reached sky high !",
                 quote28="Oops ! My feeling core just overheated !",
                 quote29="After many tests by my AI, I can affirm that this is awesome.",
                 quote30="Interesting things for sure",
                 quote31="Pictures ! Pictures everywhere !",
                 quote32="Here you go ! Enjoy !",
                 quote33="And make sure to follow the author !",
                 quote34="I dare you to make a better one ! ",
                 quote35=" -- PRIMARY CORE ERROR : TOO AMAZING TO PROCESS --",
                 quote36=" -- DEBUG MESSAGE : awesomeness value caused critical memory overflow --",
                 quote37=" -- DEBUG MESSAGE : imageQUality value is too big for double data type --",
                 quote38=" -- DEBUG MESSAGE : fImageTreatment returned error message : \"Too awesome\" --",
                 quote39=" -- Core overheated : Images are too much to handle --",
                 quote50="I am running out of ideas for texts. But here you go ! ")


superQuote = dict(
    quote1 = "Hey ! More pictures from {} ! ",
    quote2 = "{} ! One of my favorites ! ",
    quote3 = "Check out @{} ! His work is absolutely fantastic ! ",
    quote4 = " -- VALUE feelingsFor{} IS OVER AVAILABLE CAPACITY",
    quote5 = "You can feel special, {}. You're one of my favorites !"
)
#The filter
Hashtag = "EDPostcards"



datadir = os.path.dirname(f"{filepath}/data/")
if not os.path.exists(datadir):
    os.makedirs(datadir)
if not os.path.exists(f"{filepath}/dl/"):
    os.makedirs(f"{filepath}/dl")


##  MAIN FUNCTIONS
def verbose(text):
    """
        Function used to log text in a file and printing it in the console.
        Replacing usual print()
        params :
            text    : text to print
    """
    if Verbose:
        fold = os.path.dirname(f"{filepath}/logs/verbose/")
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
    fold = os.path.dirname(f"{filepath}/logs/")
    if not os.path.exists(fold):
        os.makedirs(fold)
    today = datetime.datetime.now()
    logsFile = open(f"{filepath}/logs/startup.txt", "a")
    log = f"[{today}] : Bot {__program__} v{__version__} logged in\n"
    logsFile.write(log)
    print(log, end='')

def logText(text):
    """
        Function used to log text in a file and printing it in the console.
        Replacing usual print()
        params :
            text    : text to print
    """
    fold = os.path.dirname(f"{filepath}/logs/console/")
    if not os.path.exists(fold):
        os.makedirs(fold)
    today = datetime.datetime.now()
    logsFile = open(f"{fold}/{today.year}-{today.month}-{today.day}.txt", "a")
    log = f"[{today.hour}:{today.minute}:{today.second}] {text} \n"
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
    fold = os.path.dirname(f"{filepath}/logs/errorLogs/")
    if not os.path.exists(fold):
        os.makedirs(fold)
    today = datetime.datetime.now()
    logsFile = open(f"{fold}/{today.year}-{today.month}-{today.day}.txt", "a")
    log = f"[{today.hour}:{today.minute}:{today.second}] 0x0{errnum} : {errtext}\n"
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
    folder = f"{filepath}/dl/{sender}/"
    if not os.path.exists(folder):
        os.makedirs(folder)
    today = datetime.datetime.now()

    dl_files = set()
    for url in media_files:
        i += 1
        name = f"{today.day}-{today.month}_{today.hour}h{today.minute}_{i}.jpg"
        logText(f"\n - Downloading media {i} : {url} to {folder}{name}")
        try:
            wget.download(url, out=folder+name)
            dl_files.add(name)
        except Exception as error:
            logText(str(error)+"\nUnable to download file. Cancelling.")
            logError(156, str(error)+"\nUnable to download file.")
            return False
        except:
            logText("Oops I fucked up... You didn't wanted this anyway.")
            logError(157, "Nomething bad happened...")
            return False
    media_files = set()
    return dl_files, folder

#def ftpSend(dlFiles, fold):
#    """
#        This function is used to send filed to the ftp server
#        params :
#            dlFiles : List of files to send
#            fold    : Folder
#    """
#    try:
#        session = ftplib.FTP(ADDR, IDENT, PWD)
#        session.cwd('/dev/dls/wp-content/uploads/EDPostcards')
#        #print('\n    =EDPostcards Folder')
#        #session.retrlines('LIST')
#        #print(str(session.nlst()) + '\n' + str(fold[3:-1]))
#        if fold[3:-1] not in session.nlst():
#            print('New user detected. Creating user folder')
#            session.mkd(fold[3:])
#        session.cwd(fold[3:])
#        for fName in dlFiles:
#            #fName = fold.split('/')[-1]
#            openFile = open(fold+fName, 'rb')
#            code = session.storbinary('STOR ' + fName, openFile)
#            print(f"File {fName} sent to {fold[3:]} \n{code}")
#            openFile.close()
#        session.quit()
#    except Exception as error:
#        logText(str(error))

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

def IsReply(status):
    """
    Function to test if the given object is a reply
        :param status:
    """
    if status.in_reply_to_status_id != None:
        return True
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

def dataHandler(data, main):
    """
    Function to handle data like tweets or direct messages
        :param data:
    """
    if not "friends" in data:
        if IsStatus(data) and not IsRetweet(data) and not HaveSent(me, data) and not IsReply(data) and ((not main and IsMentionned(me, data)) or (main and HaveHashTag(data, Hashtag))):
            handleImageStatus(data)
        if IsDirectMessage(data) and not HaveSent(me, data):
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
        elif cmd.lower().startswith('addfav '):
            cmdr = cmd[7:]
            userlist = config.items('BestUsers', raw=True)
            user = (cmdr, str(len(userlist)+1))
            if not user[0] in config['BestUsers']:
                userlist.append(user)
                config['BestUsers'] = dict(userlist)
                with open(f"{filepath}/data/config.cfg", 'w') as configfile:
                    config.write(configfile)
        elif cmd.lower().startswith("foo "):
            text = cmd[4:]
            logText("bar : " + text)

def quoteStatus(statusId):
    """
    Function to quote the given status
        :param statusId:
    """
    decoded = api.get_status(statusId, tweet_mode="extended")
    sendertag = decoded.user.screen_name
    text = decoded.full_text
    media = set()
    media_files = set()
    media = decoded.extended_entities["media"]

    logText("Status n"+str(statusId)+" by @"+ sendertag+ "\n\""+text+"\" ("+str(len(media)) + " media files)")
    if len(media) >= 1:                                                 #Did we got some medias ?
        for i in media:
            media_files.add(i["media_url_https"])                       #Add medias to var
        dlFiles, folder = dl(media_files, sendertag)                    #Get those medias in your files
        print(f"Folder {folder} updated : ")
        for filename in dlFiles:
            print(f" - {filename} created")
        
        if sendertag in bestUsers:
            _, qtext = random.choice(list(superQuote.items()))
            print(qtext.format(sendertag))
            api.update_status(status=f"{qtext.format(sendertag)} https://twitter.com/{sendertag}/status/{statusId}")
        else:
            _, qtext = random.choice(list(quoteText.items()))           #Get one of the quote answers
            api.update_status(status=f"{qtext} https://twitter.com/{sendertag}/status/{statusId}")
        return True
    return False

class mainStreamListener(tweepy.StreamListener): #MAIN STREAM TO HANDLE HASHTAG TREATMENT
    """
    Main Stream Class
        :param tweepy.StreamListener:
    """
    def on_data(self, status):
        decoded = json.loads(status)
        dataHandler(decoded, True)

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
        decoded = json.loads(status)
        dataHandler(decoded, False)
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
    
    try:                                                #Starting streams
        if mainStream.running or cmdStream:
            logText("Stream already running.")
            mainStream.disconnect()
            cmdStream.disconnect()
        else:
            logText("Stream not running. Starting Stream...")
    except:
        logText("Stream not Detected. Starting Stream...")

    mainStream = tweepy.Stream(auth=api.auth, listener= mainStreamListener())
    time.sleep(3) #So twitter calms down a little
    cmdStream = tweepy.Stream(auth=api.auth, listener= cmdStreamListener())

    mainStream.filter(track=[Hashtag], is_async=True)
    cmdStream.userstream(is_async=True)
    shutdown = False

    if mainStream.running:
        logText("MainStream running.")
    else:
        logText("MainStream startup failed")
        fshutdown()
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
