clear;
echo "
██████╗ ██████╗ ███████╗ █████╗ ██╗  ██╗ ██████╗ ██╗   ██╗████████╗
██╔══██╗██╔══██╗██╔════╝██╔══██╗██║ ██╔╝██╔═══██╗██║   ██║╚══██╔══╝
██████╔╝██████╔╝█████╗  ███████║█████╔╝ ██║   ██║██║   ██║   ██║   
██╔══██╗██╔══██╗██╔══╝  ██╔══██║██╔═██╗ ██║   ██║██║   ██║   ██║   
██████╔╝██║  ██║███████╗██║  ██║██║  ██╗╚██████╔╝╚██████╔╝   ██║   
╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝  ╚═════╝    ╚═╝   
Made by Jkutkut
See more at https://github.com/Jkutkut
Instalation will begin shortly.
-Making sure that Python3 and the libraries needed are installed";

echo "-Checking Python3:" &&
sudo apt install python3 &&
echo "-Checking pip3:" &&
sudo apt install python3-pip &&
echo "-Checking pygame:" &&
sudo pip3 install pygame ||
(echo "
~~~~~~~~    ERROR AT INSTALLATION   ~~~~~~~~
    Please check README.md
" && exit 1) #if error, exit



echo "-------------------------------------------
All things needed are correctly installed. Now installing the application.
" &&
echo "-Creating icon for the app" &&
sudo cp Res/logo.png /usr/share/icons/breakout.png && # move the icon to the correct dir

echo "-Creating executable" &&
chmod 755 main.py && # make it able to be executed

echo "-Creating Desktop Entry" &&
echo "[Desktop Entry]
Type=Application
Encoding=UTF-8
Name=Breakout
Comment=Made by Jkutkut
Exec=$(pwd)/main.py
Icon=/usr/share/icons/breakout.png
Terminal=false" >> breakout.desktop && # create the .desktop file

sudo mv breakout.desktop /usr/share/applications/ &&
echo "
Installation ended.
Breakout installed correctly" ||

echo "
~~~~~~~~    ERROR AT INSTALLATION   ~~~~~~~~
    Not able to install the game.
" #if error, exit