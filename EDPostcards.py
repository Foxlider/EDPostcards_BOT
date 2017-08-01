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
__program__ = "EDP Bot"
__version__ = "1.8d"

##Libraries imports
import datetime
import sys
try:
    assert sys.version_info >= (3, 4)
    import tweepy
    import wget
    import json
except ImportError:
    logError(100,__program__+"needs tweepy, wget and json to work properly. Please install them using pip install <module>. ")
    sys.exit()
except AssertionError:
    logError(101, __program__+'needs python 3.4 or greater to work properly. Please see the installation guide for your Operating System.')
    sys.exit()
import time
import random
import os

#TODO:   every text in logs

##Variables setup
if ("--verbose" in sys.argv): #Sys Args
    Verbose = True
else:
    Verbose = False
    

try:
    keysFile=open("data/keyFile.txt","r")
except Exception as error:
    print(str(error) + "\nkeyFile doesn't exists. What have you done ? Nooooo ! *couic*")
    quit();
keys=keysFile.readlines()
keysFile.close()


def verbose(text):
    """
        Function used to log text in a file and printing it in the console.
        Replacing usual print()
        params : 
            text    : text to print
    """
    if Verbose :
        dir = os.path.dirname("./logs/verbose/")
        if not os.path.exists(dir):
            os.makedirs(dir)
        today = datetime.datetime.now()
        logsFile=open(dir +"/"+ str(today.year) + "-" + str(today.month) + "-" + str(today.day) + ".txt","a")
        log = "[" + str(today.hour) + ":" + str(today.minute) + ":" + str(today.second) + "] " + text + "\n"
        logsFile.write(log)
        print(log, end='')
        logsFile.close()
        

CONSUMER_KEY = keys[0].rstrip()
CONSUMER_SECRET = keys[1].rstrip()
ACCESS_KEY = keys[2].rstrip()
ACCESS_SECRET = keys[3].rstrip()
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)
media_files = set()
bigBoss = ["Foxlidev","FoxliderAtom","ED_Postcards"] #Put here your Twitter name to be an admin

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
hashtag = "EDPostcards"



global datadir
datadir = os.path.dirname("./data/")
if not os.path.exists(datadir):
    os.makedirs(datadir)
if not os.path.exists("./dl/"):
    os.makedirs("./dl")

##Functions and classes

def dl(media_files,sender):
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
        i+=1
        name = str(today.day) + "-" + str(today.month) + "_" + str(today.hour) + "h" + str(today.minute) + "_" + str(i) + '.jpg'
        logText("downloading media "+str(i)+" : " +url + " to " + folder + name)
        try:
            wget.download(url, out = folder+name)
        except Exception as error:
            logText(str(error)+"\nUnable to download file. Cancelling.")
            logError(156, str(error)+"\nUnable to download file.")
        except:
            logText("Oops I fucked up... You didn't wanted this anyway.")
            logError(157, "Nomething bad happened...")
        dl_files.add(folder+name)
    media_files = set()
    return dl_files
   
def fshutdown():
    """
        This function is supposed to shut down the bot by disconnecting each stream.
    """
    logText("Logging off...")
    shutdown = True
    loop = False
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
    shutdown = True
    loop = False
    api.update_profile(location="In a debris field")
    mainStream.disconnect()
    cmdStream.disconnect()
    os.system("./../EDPostcards.sh")
    #fshutdown()
    #python = sys.executable
    
    #FIXME: Need to restart the program
    #os.execl(python, python, * sys.argv)

def cmdHandler(cmd, orig=True):
    """
        The cmdHandler is here to handle commands to control the BOT
        params:
            cmd     : command in text
            orig    : True if it comes from the console, False if it comes from direct messages
        calls another cmdHandler if the command is not restart or shutdown
    """
    if (cmd.lower() == "shutdown"): #TODO: Improvements for shutdown
        fshutdown()
        if not orig:
            logText("Program shutdown command called.")
            sys.exit(0) #BUG: Don't exit but dunno why
            python = sys.executable #FIXME: Using this instead
    elif (cmd.lower() == "restart" or cmd.lower() =="reboot"): #TODO: Improvements for restart
        frestart()
    else:
        if (cmd.startswith("tweet ")):
            text = cmd[6:]
            try:
                api.update_status(status=text)
            except tweepy.TweepError as error:
                logError(error.args[0][0]['code'], error.args[0][0]['message'])
        elif (cmd.startswith('quote ')):
            id = cmd[6:].split(' ')[0]
            manualStatusHandler(id)
        elif (cmd.startswith('https://twitter')):
            id = cmd.split("/")[(len(cmd.split("/"))-1)]
            manualStatusHandler(id)
        elif (cmd.startswith("foo ")):
            text = cmd[4:]
            logText(text)
        
        #if orig: #If the command was sent through the console, display the message again
            #cmdHandler(input("Command ? : \n>>>")) 
            
def logStart():
    """
        Function used to log in a file at startup
    """
    dir = os.path.dirname("./logs/")
    if not os.path.exists(dir):
        os.makedirs(dir)
    today = datetime.datetime.now()
    logsFile=open("./logs/startup.txt","a")
    log="[" + str(today) + "] : Bot " + __program__ + " v" + __version__ + " logged in\n"
    logsFile.write(log)
    print(log,end='')

def logText(text):
    """
        Function used to log text in a file and printing it in the console.
        Replacing usual print()
        params : 
            text    : text to print
    """
    dir = os.path.dirname("./logs/console/")
    if not os.path.exists(dir):
        os.makedirs(dir)
    today = datetime.datetime.now()
    logsFile=open(dir +"/"+ str(today.year) + "-" + str(today.month) + "-" + str(today.day) + ".txt","a")
    log = "[" + str(today.hour) + ":" + str(today.minute) + ":" + str(today.second) + "] " + text + "\n"
    logsFile.write(log)
    print(log, end='')
    logsFile.close()

def logError(errnum = 0, errtext=""):
    """
        Function used to print errors in a file
        params: 
            errnum      : code of the error between 100 and 999
            errtext     : details of the error
    """
    dir = os.path.dirname("./logs/errorLogs/")
    if not os.path.exists(dir):
        os.makedirs(dir)
    today = datetime.datetime.now()
    logsFile=open(dir +"/"+ str(today.year) + "-" + str(today.month) + "-" + str(today.day) + ".txt","a")
    log = "[" + str(today.hour) + ":" + str(today.minute) + ":" + str(today.second) + "] 0x0" + str(errnum) + " : " + errtext + "\n"
    logsFile.write(log)
    print(log, end='')
    logsFile.close()

def statusTreatment(decoded):
    """
        specific status treatment function.
        callend to handle the hashtag when needed
        params : 
            decoded     : The status
    """
    id = decoded["id"]                                                  #IMPORTANT DATA VARS
    text = decoded["text"]                                              #|
    sender = decoded["user"]["name"]                                    #|
    sendertag = decoded["user"]["screen_name"]                          #|
    #dump(decoded)
    logText(hashtag + " in status text")                               #Write to logs
    media = set()
    media_files = set()
    if ("extended_tweet" in decoded):
        verbose("extended_tweet !")
        if ("extended_entities" in decoded["extended_tweet"]):                                #if medias were sent
            verbose("extended_entities in tweet")
            media = decoded["extended_tweet"]["extended_entities"]["media"]       #go get 'em
        elif ("media" in decoded["entities"]):
            verbose("entities in tweet")
            media = decoded["entities"]["media"]
    else:
        if ("extended_entities" in decoded):                                #if medias were sent
            verbose("extended_entities in tweet")
            media = decoded["extended_entities"]["media"]                            #go get 'em
        elif ("media" in decoded["entities"]):
            verbose("entities in tweet")
            media = decoded["entities"]["media"]
    logText("Status n°"+str(id)+" by @"+ sender + "\n\""+text+"\" ("+str(len(media)) + " media files)")
    if (len(media)>=1):                                                 #Did we got some medias ?
        for i in media:
            media_files.add(i["media_url_https"])                       #Add medias to var
        dl(media_files,sender)                                          #Get those medias in your files
        qcode, qtext = random.choice(list(quoteText.items()))           #Get one of the quotenswers
        api.update_status(status = qtext+" https://twitter.com/"+sendertag+"/status/"+str(id))

        
def manualStatusHandler(id):
    """
        manual status handler function.
        called by the cmdHandler when cmd quote is called. 
        params : 
            decoded     : The status
    """
    try:
        decoded = api.get_status(id)
        dump(decoded)
        id = decoded.id
        sendertag = decoded.author.screen_name
        if(hasattr(decoded, 'extended_entities')):
            try:
                media = decoded.extended_entities["media"]
                dump(decoded.extended_entities["media"])
                dump(decoded.entities["media"])
                media_files=set()
                sender = decoded.user.name
                if (len(media)>=1):                                                 #Did we got some medias ?
                    for i in media:
                        media_files.add(i["media_url"])                             #Add medias to var
                    dl(media_files,sender)                                          #Get those medias in your files
            except Exception as error:
                logText("Oops ! I slipped in a "+str(error))
                logError(123, str(error))
            qcode, qtext = random.choice(list(quoteText.items()))           #Get one of the quote answers
            api.update_status(status = qtext+" https://twitter.com/"+sendertag+"/status/"+str(id))
            logText("Manually quoting " + sendertag + "'s tweet " + str(id))
        else:
            logText("No media in "+ sendertag + "'s tweet " + str(id))
    except tweepy.TweepError as error:
        logError(error.args[0][0]['code'], error.args[0][0]['message'])
        
def statusHandler(decoded):
    """
        main status treatment function.
        called to handle every status received and calling statusTreatment if needed
        params : 
            decoded     : The status
    """
    dump(decoded)
    id = decoded["id"]                                                  #IMPORTANT DATA VARS
    if ("extended_tweet" in decoded):
        verbose("Extended tweet")
        text = decoded["extended_tweet"]["full_text"]
    else:
        verbose("Standard tweet")
        text = decoded["text"]                                              #|
    sender = decoded["user"]["name"]                                    #|
    sendertag = decoded["user"]["screen_name"]                          #|
    verbose(text)
    if (sendertag == me.screen_name):                                   #IF BOT sending tweets to itself
        #api.send_direct_message(screen_name=sendertag, text="Sending tweets yourself again ?")
        logText("Receiving tweet from myself : " + text)
    elif ("#" + lower(hashtag) in lower(text) and not text.startswith("RT ") ):      #MAIN : hashtag handling / not an RT
        statusTreatment(decoded)
        #print("oui")
        
def directMessageHandler(decoded):
    """
        direct messages treatment function.
        called to handle every direct message received
        params : 
            decoded     : The status
    """
    id = decoded["direct_message"]["id"]                            #IMPORTANT DATA VARS
    text = decoded["direct_message"]["text"]                        #|
    sender = decoded["direct_message"]["sender"]["name"]            #|
    sendertag = decoded["direct_message"]["sender"]["screen_name"]  #|
    logText("Direct Message n°"+str(id)+"\n\""+text+"\"")           #Write to logs
    if sendertag in bigBoss and sendertag != me.screen_name:        #IF PV sent by me and not by the BOT (avoid repeating commands)
        logText ("Receiving direct message from admin : "+text)     #Write to logs
        api.send_direct_message(screen_name=sendertag, text="Handling "+text+" command... Please wait...")                                                 #Send message
        cmdHandler(text, False)                                     #cmdHandler will se if a command is sent or not

class mainStreamListener(tweepy.StreamListener): #MAIN STREAM TO HANDLE HASHTAG TREATMENT
    #TODO: Make functions to handle treatments
    def on_data(self, status):
        #dump(self)
        decoded = json.loads(status)                                #Decode from json
        #print("====================")                               #Separator          
        #dump(decoded)                                              #UNCOMMENT THIS TO DUMP DATA
        if("direct_message" in decoded):                        #======= DATA IS DIRECT MESSAGE
            directMessageHandler(decoded)
        elif("in_reply_to_status_id" in decoded and not "event" in decoded): #======= DATA IS STATUS
            statusHandler(decoded)
        #TODO: Improve tweets
        
    def on_error(self, status_code):
        logText ("Error Code: " + str(status_code))
        logError(status_code, "Twitter API error. Refer to dev.twitter.com for more informations")
        if status_code == 420:
            return False
        else:
            return True

    def on_timeout(self):
        logError(105, 'Timeout...')
        return True
        
class cmdStreamListener(tweepy.StreamListener): #THIS ONE IS USED FOR COMMANDS HANDLING ONLY
    def on_data(self, status):
        #dump(self)
        decoded = json.loads(status)                                #Decode from json
        #print("====================")                               #Separator          
        #dump(decoded)                                              #UNCOMMENT THIS TO DUMP DATA
        if("direct_message" in decoded):                        #======= DATA IS DIRECT MESSAGE
            directMessageHandler(decoded)
    def on_error(self, status_code):
        logText ("Error Code: " + str(status_code))
        logError(status_code, "Twitter API error. Refer to dev.twitter.com for more informations")
        if status_code == 420:
            return False
        else:
            return True
    def on_timeout(self):
        logError(105, 'Timeout...')
        return True
        
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
        verbose ( '%s{' % ((nested_level) * spacing))
        for k, v in obj.items():
            if hasattr(v, '__iter__'):
                verbose(  '%s%s:' % ((nested_level + 1) * spacing, k))
                dump(v, nested_level + 1, output)
            else:
                verbose ( '%s%s: %s' % ((nested_level + 1) * spacing, k, v))
        verbose (  '%s}' % (nested_level * spacing))
    elif type(obj) == list:
        verbose (  '%s[' % ((nested_level) * spacing))
        for v in obj:
            if hasattr(v, '__iter__'):
                dump(v, nested_level + 1, output)
            else:
                verbose (  '%s%s' % ((nested_level + 1) * spacing, v))
        verbose ('%s]' % ((nested_level) * spacing))
    else:
        verbose(  '%s%s' % (nested_level * spacing, obj))

## The bot itself  

logText("BOT " + __program__ + " v" + __version__ + " started. \nConnection...")
logStart()
verbose("BOT " + __program__ + " v" + __version__ + " started. \nVerbose activated")
try:
        
    try:
        api.update_profile(location="Sol")
        me = api.me()
        logText("Logged in as @"+ me.screen_name +" !")
        #print (vars(me))
    except tweepy.TweepError:
        logText ("Could not authenticate you. \nExiting the program.")
        logError(420, str(tweepy.TweepError)+" Could not authenticate you.")
        exit()
    logText("____[ INFORMATIONS ]____")
    logText("@"+me.screen_name)
    logText(str(me.followers_count)+" followers : ")
    for follower in me.followers():
       logText(" -"+follower.screen_name)
       if (not follower.following):
            try:
                follower.follow()
            except tweepy.TweepError:
                logError(421, str(tweepy.TweepError)+" Follow error.")

    try:
        if mainStream.running or cmdStream:
            logText ("Stream already running.")
            mainStream.disconnect()
            cmdStream.disconnect()
        else:
            logText("Stream not running. Starting Stream...")
    except:
        logText("Stream not Detected. Starting Stream...")

    mainStream = tweepy.Stream(auth = api.auth, listener=mainStreamListener())
    cmdStream = tweepy.Stream(auth = api.auth, listener=cmdStreamListener())

    mainStream.filter(track=[hashtag], async=True)
    cmdStream.userstream(async=True)
    shutdown = False

    if mainStream.running:
        logText ("MainStream running.")
    else:
        logText("MainStream startup failed")
        fshutdown()
    if cmdStream.running:
        logText ("CMDStream running.")
    else:
        logText("CMDStream startup failed")
        fshutdown()
    time.sleep(2)


    #cmdHandler(input("Command ? : \n>>>"))
except ReadTimeoutError :
    frestart()
