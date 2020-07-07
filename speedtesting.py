#! /usr/bin/python3
# -*- coding: <UTF-8> -*-

# @author: Victor F. Teran Herrera
# @write your enquieres to: vteran93 at yahoo dot es 
# Version: 0.1
# Github: Pending
"""
    #### README ####
    To execute you need python3 (testend on python 3.6.9)
    For windows you should downloaded from https://www.python.org/downloads/


    > python3 speedtesting.py 

    ## Automate executing and saving results to csv ##

        # Windows #
        If you want to program periodic task to run in automated way, you need to:
            https://www.howtogeek.com/405806/windows-task-manager-the-complete-guide/
        
        # Linux
        Just use crontab 
"""

"""
#### Licence

Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)
This is a human-readable summary of (and not a substitute for) the license.
https://creativecommons.org/licenses/by-nc/4.0/legalcode

Disclaimer
----------

You are free to:
Share - copy and redistribute the material in any medium or format
Adapt - remix, transform, and build upon the material
The licensor cannot revoke these freedoms as long as you follow the license terms.
Under the following terms:

Attribution 
-----------

You must give appropriate credit, provide a link to the license, and indicate if changes were made.
You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.

NonCommercial
-------------

You may not use the material for commercial purposes.

No additional restrictions -
You may not apply legal terms or technological measures that legally restrict others from doing 
anything the license permits.

Notices
-------

You do not have to comply with the license for elements of the material in the public domain or where
your use is permitted by an applicable exception or limitation.
No warranties are given. The license may not give you all of the permissions necessary for your intended use.
For example, other rights such as publicity, privacy, or moral rights may limit how you use the material.

"""

import gi
gi.require_version('Notify', '0.7')


import os
import csv
import random
from datetime import datetime
from gi.repository import Notify


import xml.etree.ElementTree as ET

import speedtest

# This file was taken from https://c.speedtest.net/speedtest-servers-static.php
SERVERS_FILE_LIST = '/home/victor.teran/speedtest/servers.xml'
ADRESS_TO_WRITE_RESULTS = '/home/victor.teran/speedtest/speed_testing_results.csv'

FRONTIER_MIAMI = 14231
FRONTIER_MIAMI = 14237
ORANGE_MOSCOW =  10366
ORANGE_MADRID = 14979


def convert_bytes(num):
    """
    this function will convert bytes to MB.... GB... etc
    """
    step_unit = 1000.0 #1024 bad the size

    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < step_unit:
            return "%3.1f %s" % (num, x)
        num /= step_unit


def build_row(results_dict, keys_to_save):
    row = []
    for key in keys_to_save:
        if key in ('download', 'upload'):
            row.append(convert_bytes(results_dict.get(key, 0)))
        elif key in ('download_bytes', 'upload_bytes'):
            if key == 'download_bytes':
                row.append(results_dict.get('download', 0))
            else:
                row.append(results_dict.get('upload', 0))
        elif key == 'timestamp_colombia':
            row.append(str(datetime.now()))
        else:
            row.append(results_dict.get(key, False))
    return row


def write_file(row, file_name):
    if not os.path.isfile(file_name):
        f = open(file_name, 'a+')
        with f:
            writer = csv.writer(f)
            writer.writerows([keys_to_save])
            writer.writerows(rows)
    else:
        f = open(file_name, 'a+')
        with f:
            writer = csv.writer(f)
            writer.writerows(rows)


def send_request(servers=[], fallback_message=''):
    
    threads = None
    results_dict = {}
    try:
        s = speedtest.Speedtest()
        s.get_servers(servers)
        s.get_best_server()

        s.download(threads=threads)

        s.upload(threads=threads)
        s.results.share()
        results_dict = s.results.dict()

        results_dict['exception'] = fallback_message if fallback_message else False

    except speedtest.ShareResultsSubmitFailure as e:
        return send_request(fallback_message=e)
    except Exception as e:
        results_dict['exception'] = e

    return results_dict


def notificate(results):
    Notify.init("Speed Test Script")
    if results[-2]:
        speed_test_notification = Notify.Notification.new("Speedtest",
                                    f"Error: {row[-2]}",
                                    "dialog-error")
    else:
        speed_test_notification = Notify.Notification.new("Speedtest",
                                    f'Download  {row[1]}, Upload {row[2]}',
                                    "dialog-information")
    speed_test_notification.set_timeout(3)
    speed_test_notification.show()


def get_servers_ids():
    tree = ET.parse(SERVERS_FILE_LIST)
    root = tree.getroot()

    return [int(server.attrib['id']) for server in root[0]]


def get_random_server(servers_id):
    return random.choice(servers_id)

keys_to_save = ['timestamp_colombia',
                'download',
                'upload',
                'download_bytes',
                'upload_bytes',
                'ping',
                'server',
                'timestamp',
                'bytes_sent',
                'bytes_received',
                'share',
                'exception',
                'client']


servers_id = get_servers_ids()
FRONTIER_MIAMI, 
FRONTIER_MIAMI, 
ORANGE_MOSCOW,
ORANGE_MADRID,

selected_server = [
    get_random_server(servers_id),
    FRONTIER_MIAMI, 
    FRONTIER_MIAMI, 
    ORANGE_MOSCOW,
    ORANGE_MADRID,
]
results_dict = send_request(selected_server)
row = build_row(results_dict, keys_to_save)
rows = [row]
print(f'{str(datetime.now())} Download {row[1]}, Upload {row[2]}')
write_file(rows, ADRESS_TO_WRITE_RESULTS)
# To launch notifications throught Ubuntu Linux GDM Gnome3
# BUG Does not work on linux or under crontab (need testing) 
# TODO Send notifications to Windows 10 bar 
notificate(row)
