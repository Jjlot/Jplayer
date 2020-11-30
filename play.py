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
import media_list

from pynput import keyboard
from flask import Flask
from threading import Thread

# @ -------- DATABASE --------
"""
CREATE TABLE IF NOT EXISTS `list`(
   `id` INT UNSIGNED AUTO_INCREMENT,
   `path` VARCHAR(100) NOT NULL,
   `weight` INT NOT NULL,
   PRIMARY KEY ( `id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
"""

# @ -------- DEPENDENCY --------
"""
pip3 install python-vlc
pip3 install pynput
pip3 install flask
pip3 install python-xlib
pip3 install system_hotkey

yum install kernel-headers-$(uname -r) -y
yum install gcc -y
yum install python-devel

sed -i 's/geteuid/getppid/' /usr/bin/vlc
"""

# @ -------- GLOBAL --------
media_player = None
jump = False

# @ -------- CONFIG --------
# run_mode = 'local'
run_mode = 'remote'
directory = "/home/"
debug_mode = False
nfs_ip = "192.168.0.102"
nfs_dir = "/media/slot3_4t/media"
local_dir = "/home/pi/Desktop/nfs"

# @ -------- CONFIG end --------

# @ -------- HOTKEYS --------
# The key combination to check
COMBINATIONS = [
    {keyboard.Key.ctrl, keyboard.KeyCode(char='q')},
    {keyboard.Key.ctrl, keyboard.KeyCode(char='Q')}
]

# The currently active modifiers
current = set()


def execute():
    global media_player
    global jump
    jump = True
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


# @ -------- RESTAPI --------
app = Flask(__name__)


@app.route('/')
def hello_world():
    return "hello world"


@app.route('/title/', methods=['GET'])
def rest_get_title():
    return str(media_player.get_title())


# curl --request POST 127.0.0.1:5000/next/
@app.route('/next/', methods=['POST'])
def rest_post_next():
    return str(media_player.stop())


def web_server():
    app.run()


# @ -------- WHAT --------
def mount_nfs():
    # Mount nfs
    print(" Mounting nfs")
    while os.system("mount | grep " + local_dir) != 0:
        cmd = "sudo mount -t nfs " + nfs_ip + ":" + nfs_dir + " " + local_dir
        print("run-cmd: ", cmd)
        os.system(cmd)
        time.sleep(5)


def _play(video):
    print('playing: %s', video)

    global media_player
    global jump
    jump = False

    # creating Instance class object 
    player = vlc.Instance()

    # creating a new media 
    media = player.media_new(video)

    # creating a media player object 
    media_player = player.media_player_new()

    media_player.set_media(media)

    media_player.set_video_title_display(3, 8000)

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

    media_player.stop()
    return


def test():
    print('in test')
    # Test
    import random

    r = random.randint(1, 10000)
    media_name = 'name' + str(r)
    media_path = 'path' + str(r)

    m = media_list.MediaList()
    m.create(path=media_path, name=media_name)

    vid = m.get_id_by_path(media_path)
    m.increase_fail_count(vid)
    m.increase_play_count(vid)
    m.increase_jump_count(vid)
    # m.update_priority(vid)
    m.update_priority(vid, action='low')
    m.update_name(vid, 'a new name')

    list_all = m.get_list_all()
    for one in list_all:
        # print('-' * 20)
        m.show_info(one)
        # print(one.name)
        m.delete_by_id(one.id)


def update_database(contents):
    m = media_list.MediaList()
    for content in contents:
        vid = m.get_id_by_path(content)
        if vid:
            pass
        else:
            m.create(path=content)

    list_all = m.get_list_all()
    for one in list_all:
        # print('-' * 20)
        m.show_info(one)
        # print(one.name)
        # m.delete_by_id(one.id)


if __name__ == '__main__':
    opts, args = getopt.getopt(sys.argv[1:], '-h-f:-d', ['help', 'filename=', 'debug'])
    # print(opts)
    for opt_name, opt_value in opts:
        if opt_name in ('-h', '--help'):
            print("[*] Help info")
        if opt_name in ('-d', '--debug'):
            print(" Debug mode ")
            debug_mode = True

        if opt_name in ('-f', '--filename'):
            fileName = opt_value
            print("[*] Filename is ", fileName)
            # do something

    if run_mode == 'remote':
        mount_nfs()

    test_path = "/home/src/jnote/test"
    print(test_path)

    # global jump

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

    # 2.5 update database
    update_database(contents)
    exit(0)

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

                if jump:
                    break

        else:
            print(" Something error")
