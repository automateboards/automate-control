#!/bin/bash

if [ `whoami` != root ]; then
 echo "Please run with sudo!"
 exit 1
fi

#python3 -m compileall -b AutomateControl

WORKDIR="$(dirname "$0")"
HOMEDIR=$(echo $HOME)

echo $HOMEDIR
echo $WORKDIR

cd $WORKDIR

DESTPATH_APPDATA=$HOMEDIR"/.local/share/automatectrl/"
DESTPATH_BIN=$HOMEDIR"/.local/bin/automatectrl"

echo $DESTPATH_APPDATA
echo $DESTPATH_BIN

# ------ Install files to the correct location -------
# ----------------------------------------------------

# Copy application
echo "Copy appdate"
mkdir -p $DESTPATH_APPDATA
cp -v -R  * $DESTPATH_APPDATA
chmod 755 -R $DESTPATH_APPDATA

# Copy executable
echo "Copy executable"
cp -v ./bin/automatectrl $DESTPATH_BIN
chmod 755 $DESTPATH_BIN

# --- Install the required distribution packages -----
# ----------------------------------------------------

echo "Installing required distribution packages"
apt-get update

if [ ! -e /usr/bin/pip3 ]; then
    apt-get -y install python3-pip
fi

# --------- Install required python packages ---------
# ----------------------------------------------------

echo "Installing required python packages"

pip3 show PySimpleGUI 1>/dev/null
if [ $? != 0 ]; then
    pip3 install PySimpleGUI==4.38.0
fi

pip3 show screeninfo 1>/dev/null
if [ $? != 0 ]; then
    pip3 install screeninfo==0.6.7
fi

pip3 show pyserial 1>/dev/null
if [ $? != 0 ]; then
    pip3 install pyserial
fi

pip3 show smbus 1>/dev/null
if [ $? != 0 ]; then
    pip3 install smbus
fi

echo "Done!"
