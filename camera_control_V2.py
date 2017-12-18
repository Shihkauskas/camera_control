#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
import socket
import logging
import smtplib
import list_cameras
from termcolor import colored
from concurrent.futures import ThreadPoolExecutor


class Logg():
    def __init__(self, ip):
        self.ip = ip

    def log_off(self):
        name_camera = list_cameras.cameras.setdefault(self)
        with open('log.txt', 'r')as f:
            log = f.readlines()
            log = ''.join([i for i in log])
        if self not in log:
            email(self, name_camera)
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


def connect(link, port, results=None, results1=None):
    try:
        socket.socket().connect((link, port))
        if results is not None:
            results.append(link)
        return True
    except:
        results1.append(link)
        return False


def email(ip, name_camera):
    fromaddr = 'Mr. Camera-control Robot <***>'
    toaddr = 'Administrator <***>'
    subj = 'Camera CRASH!'
    msg_txt = 'Camera ' + ip + ' -- ' + name_camera + ' OFFLINE'
    msg = "From: %s\nTo: %s\nSubject: %s\n\n%s" % (fromaddr, toaddr, subj, msg_txt)
    username = '***'
    password = '***'
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    try:
        server.login(username, password)
        server.sendmail(fromaddr, toaddr, msg)
        server.quit()
    except:
        pass


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
    os.system('x-terminal-emulator -e python logs_screen.py')
    while True:
        camera_scan()
        time.sleep(600)
        os.system('clear')
