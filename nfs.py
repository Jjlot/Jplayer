import os
import time

from configparser import ConfigParser
from prettytable import PrettyTable


class Nfs(object):
    def __init__(self, local_dir, config_file):
        self.local_dir = local_dir
        print(' NFS runs in path: ', self.local_dir)

        cfg = ConfigParser()
        cfg.read(config_file)

        cs = cfg.__getitem__('nfs')

        self.nfs_ip = cs.get('ip')
        self.nfs_dir = cs.get('dir')
        self.ignore = cs.get('ignore').replace(" ", "").split(',')

        table = PrettyTable()
        table.add_column('key', ['ip', 'dir', 'ignore'])
        table.add_column('value', [self.nfs_ip, self.nfs_dir, self.ignore])
        print(table)

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

        raw_dirs = os.listdir(self.local_dir)
        dirs = list(set(raw_dirs) - set(self.ignore))
        print(" p1: ", dirs)

        classifies = []
        for directory in dirs:
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
