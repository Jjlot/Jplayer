import os
import time


class Nfs(object):
    def __init__(self, local_dir):
        print("run with local path: ")

        # Should get from config file.
        self.nfs_ip = "192.168.0.102"
        self.nfs_dir = "/media/slot3_4t/media"
        self.local_dir = local_dir

    def get_list(self):
        return self.scan_path()

    def mount(self):
        # Mount nfs
        print(" Mounting nfs")
        while os.system("mount | grep " + self.local_dir) != 0:
            cmd = "sudo mount -t nfs " + self.nfs_ip + ":" + self.nfs_dir + " " + self.local_dir
            print("run-cmd: ", cmd)
            os.system(cmd)
            time.sleep(5)

    def scan_path(self):
        # 1. Find the root media directories
        print(" Walking in path: ", self.local_dir)

        directories = os.listdir(self.local_dir)
        print(" p1: ", directories)

        classifies = []
        for directory in directories:
            abs_dir = self.local_dir + "/" + directory
            # print(" Scan directory: " + abs_dir)
            if os.path.isdir(abs_dir):
                # print(" New classify directory")
                classifies.append(abs_dir)

        print(" p2: ", str(classifies))

        # 2. Get all the play contents
        contents = []
        for classify in classifies:
            ones = os.listdir(classify)
            for one in ones:
                contents.append((classify + "/" + one)[len(self.local_dir):])

        return contents
