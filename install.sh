#!/bin/bash

### Description: FoxliBOT installation tool for FoxliBOT v2.2b and greater
### Written by: Foxlider Atom


clear
echo -e "\n\n\t\t____[ EDPostcards installation tool v0.1b ]____\n\n"
maindir=$PWD
cd $maindir



#CHECKING keyfile
if [ -f "$maindir/data/config.cfg" ]
then
    echo "Key file is already created. Will not overwrite manually created files."
else
    echo "You will be redirected to the Twitter Apps webpage in a few seconds..."
    URL=https://apps.twitter.com/app/13667962/keys
    if which xdg-open > /dev/null 
    then
        xdg-open $URL
    elif which gnome-open > /dev/null  
    then
        gnome-open $URL
    else
        echo "Could not detect the web browser to use."
        exit 1
    fi
#CREATING keyfile
    echo "Please log in and type the requested keys :  "
    mkdir "keys"
    cd "$maindir/data/"
    echo ' - Enter the Consumer Key : '
    token="Consumer key"
    read token
    echo "[Keys]" >> config.cfg
    echo -e "CONSUMER_KEY = $token" >> config.cfg
    
    echo ' - Enter the Consumer Secret : '
    token="Consumer secret"
    read token
    echo -e "CONSUMER_SECRET = $token" >> config.cfg
    
    echo ' - Enter the Access Token : '
    token="Access Token"
    read token
    echo -e "ACCESS_KEY = $token" >> config.cfg
    echo ' - Enter the Access Token Secret : '
    token="Access Secret"
    read token
    echo -e "ACCESS_SECRET = $token" >> config.cfg
    echo "[BestUsers]" >> config.txt
    echo "FoxliderAtom = 1" >> config.cfg
    cd ".."
fi
#CREATING folders
echo "Processing..."
mkdir "data"
mkdir "dl"
mkdir "logs"
mkdir "logs/verbose"
mkdir "logs/console"
echo " - Directories created"
echo " - Files created"

#CREATING launchscript
launchscript="#!/bin/bash\n#EDPostcards launcher\n\ngit fetch --all\ngit reset --hard origin/master\ngit pull origin master\ncd $maindir\nkonsole --noclose -e \"python3 EDPostcards.py\""

cd $maindir
echo -e $launchscript > EDPostcards.sh
chmod +x EDpostcards.sh
echo " - Launcher created"

#INSTALLING dependencies
sudo python3 -m pip install wget
sudo python3 -m pip install configparser

echo -e "\n\n\tDone."
echo "Press Enter to quit"
read
