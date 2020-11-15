from threading import Thread
import os
import time

scan_idle = 3
disk_path='/'
directory = "/home/"
debug_mode = False
nfs_ip = "192.168.0.102"
nfs_dir = "/media/slot3_4t/media"



class UpdateList():
    def __init__(self, run_mode='local'):
        print("-------->update-list init start")

        if run_mode == 'remote':
            self.mount_nfs()

        self._running = True
        t = Thread(target=self.run)
        t.start()

    def terminate(self):
        self._running = False

    def run(self):
        print('-------->start running')
        count = 0
        while self._running:
            time.sleep(1)
            print('running', count)
            count += 1
            if not count % scan_idle:
                self.scan_disk()

    def mount_nfs():
        # Mount nfs
        print(" Mounting nfs")
        while os.system("mount | grep " + local_dir) != 0 :
            os.system("sudo mount -t nfs " + nfs_ip + ":" + nfs_dir + " " + local_dir)

    '''
    /path/classify/content
    classify is the absolute name of directory
    '''
    def scan_path(self, path):
        # 1. Find the root media directories
        print(" Walking in path: " + path)

        directories = os.listdir(path)
        print(directories)

        classifies = []
        for directory in directories:
            abs_dir = path + "/" + directory
            # print(" Scan directory: " + abs_dir)
            if os.path.isdir(abs_dir):
                # print(" New classify directory")
                classifies.append(abs_dir)

        print(" Got the classifies: " + str(classifies))

        # 2. Get all the play contents
        contents = []
        for classify in classifies:
            ones = os.listdir(classify)
            for one in ones:
                contents.append(classify + "/" + one)

        return contents

    def scan_disk(self):
        print('--------->start scan disk')
        contents = []
        for path in paths.splite(',')
            contents.append(self.scan_path(path))

        self.compare_to_db(contents)

    def compare_to_db(self):
        print('-------->start compare_to_db')
        # get all from db
        # get difference from db
        # update to db

u = UpdateList(debug_mode=True)
time.sleep(8)
u.terminate()
