import os
import syslog
import random
import time
import getopt
import sys
import vlc
import functools
import termios
import tty

from pynput import keyboard
from flask import Flask
from threading import Thread


#@ -------- DEPENDENCY --------
"""
pip install pynput

pip install flask

yum install kernel-headers-$(uname -r) -y
yum install gcc -y
yum install python-devel
pip install python-xlib
pip install system_hotkey
"""

#@ -------- GLOBAL --------
media_player = None



#@ -------- CONFIG --------
# run_mode = 'local'
run_mode = 'remote'
directory = "/home/"
debug_mode = False
nfs_ip = "192.168.0.102"
nfs_dir = "/media/slot3_4t/media"
local_dir = "/home/pi/Desktop/nfs"

#@ -------- CONFIG end --------

#@ -------- HOTKEYS --------
# The key combination to check
COMBINATIONS = [
    {keyboard.Key.ctrl, keyboard.KeyCode(char='q')},
    {keyboard.Key.ctrl, keyboard.KeyCode(char='Q')}
]

# The currently active modifiers
current = set()

def execute():
    print ("Do Something")

    global media_player
    media_player.stop()
def on_press(key):
    if any([key in COMBO for COMBO in COMBINATIONS]):
        current.add(key)
        if any(all(k in current for k in COMBO) for COMBO in COMBINATIONS):
            execute()

def on_release(key):
    if any([key in COMBO for COMBO in COMBINATIONS]):
        current.remove(key)

def hotkey_listener():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


#@ -------- RESTAPI --------
app = Flask(__name__)

@app.route('/')  
def hello_world():
    return "hello world"

@app.route('/title/',methods=['GET'])
def rest_get_title():
    return str(media_player.get_title())

# curl --request POST 127.0.0.1:5000/next/
@app.route('/next/',methods=['POST'])
def rest_post_next():
    return str(media_player.stop())

def web_server():
    app.run()


#@ -------- WHAT --------
def mount_nfs():
    # Mount nfs
    print(" Mounting nfs")
    while os.system("mount | grep " + local_dir) != 0 :
        os.system("sudo mount -t nfs " + nfs_ip + ":" + nfs_dir + " " + local_dir)
        time.sleep(5)

def _play(video):
    global media_player

    # creating Instance class object 
    player = vlc.Instance() 

    # creating a new media 
    media = player.media_new(video)

    # creating a media player object 
    media_player = player.media_player_new() 

    media_player.set_media(media) 

    media_player.set_video_title_display(3, 3000)

    # media_player.set_fullscreen(True)

    # start playing video 
    media_player.play() 
    time.sleep(1)
    duration = 1000
    mv_length = media_player.get_length() - 1000
    print(str(mv_length / 1000) + "s")

    while duration < mv_length:
        time.sleep(1)
        duration = duration + 1000
        status = media_player.get_state()

        # print(status)
        if media_player.get_state() != vlc.State.Playing:
            media_player.stop()
            return

if __name__ == '__main__':

    opts,args = getopt.getopt(sys.argv[1:],'-h-f:-d',['help','filename=','debug'])
    # print(opts)
    for opt_name,opt_value in opts:
        if opt_name in ('-h','--help'):
            print("[*] Help info")
        if opt_name in ('-d','--debug'):
            print(" Debug mode ")
            debug_mode = True

        if opt_name in ('-f','--filename'):
            fileName = opt_value
            print("[*] Filename is ",fileName)
            # do something

    if run_mode == 'remote':
        mount_nfs()

    test_path = "/home/src/jnote/test"
    print(test_path)

    # start_play(test_path)

    # 1. Find the root media directories
    # path = test_path
    path = local_dir
    # print(" Walking in path: " + path)

    directories = os.listdir(path)

    # print(directories)
    classifies = []
    for directory in directories:
        abs_dir = path + "/" + directory
        # print(" Scan directory: " + abs_dir) 
        if os.path.isdir(abs_dir):
            # print(" New classify directory")
            classifies.append(abs_dir)
            # _play(d1)

    # print(" Got the classifies: " + str(classifies)) 

    # 2. Get all the play contents
    contents = [] 
    for classify in classifies:
        ones = os.listdir(classify)
        for one in ones:
            contents.append(classify + "/" + one)    
    # print(contents)

    # 3. Set to random
    contents = random.sample(contents, len(contents))
    print(contents)

    # 3.5 Start hot_key listener
    t = Thread(target=hotkey_listener)
    t.start()

    # 3.6 Start web interface
    t2 = Thread(target=web_server)
    t2.start()


    # 4. Play
    for content in contents:
        if os.path.isfile(content):
            # print(" It's a file")
            _play(content)

        elif os.path.isdir(content):

            # print(" It's a directory")
            files = os.listdir(content)
            files.sort()

            for file in files:
                abs_path = content + "/" + file
                _play(abs_path)

        else:
            print(" Something error")


