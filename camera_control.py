#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
import socket
import logging
import list_cameras
from termcolor import colored
from concurrent.futures import ThreadPoolExecutor


def connect(link, port, results=None, results1=None):
    try:
        socket.socket().connect((link, port))
        if results is not None:
            results.append(link)
        return True
    except:
        results1.append(link)
        return False


class Logg():
    def __init__(self, ip):
        self.ip = ip

    def log_off(self):
        name_camera = list_cameras.cameras.setdefault(self)
        with open('log.txt', 'r')as f:
            log = f.readlines()
            log = ''.join([i for i in log])
        if self not in log:
            with open('log.txt', 'a')as file:
                file.write(self + '\n')
                logging.basicConfig(filename='Full_log.log',
                                    level=logging.INFO,
                                    format='%(message)s  |  %(asctime)s',
                                    datefmt='%Y.%m.%d %H:%M:%S')
                logging.info(name_camera + ' -- ' + self)

    def log_on(self):
        with open('log.txt', 'r')as f:
            log = f.readlines()
            log = ''.join([i for i in log])
        if self in log:
            with open('log.txt', 'w')as file:
                file.write(log.replace(self, ''))


def camera_scan():
    ip_on = []
    ip_off = []
    host = list_cameras.cameras.keys()
    socket.setdefaulttimeout(0.5)
    with ThreadPoolExecutor(max_workers=512) as executor:
        for link in host:
            executor.submit(connect, link, 80, ip_on, ip_off)

    ip_on.sort()
    ip_off.sort()

    for ip in ip_on:
        name_camera = list_cameras.cameras.setdefault(ip)
        Logg.log_on(ip)
        if len(ip) == 12:
            print(colored(ip, 'green'), ' --', colored(name_camera, 'green'))
        else:
            print(colored(ip, 'green'), '--', colored(name_camera, 'green'))

    print('\n', colored('`' * 40, 'blue'), '\n')

    for ip in ip_off:
        name_camera = list_cameras.cameras.setdefault(ip)
        Logg.log_off(ip)
        if len(ip) == 12:
            print(colored(ip, 'red'), ' --', colored(name_camera, 'red'))
        else:
            print(colored(ip, 'red'), '--', colored(name_camera, 'red'))

if __name__ == "__main__":
    # subprocess.Popen use better
    os.system('x-terminal-emulator -e python logs_screen.py')
    while True:
        camera_scan()
        time.sleep(600)
        os.system('clear')
        
