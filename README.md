# hammerDOS
**hammer.py** just keeps sending get/post requests to the web server via socket module.

**slowloris.py** tries to establish a connection and keep the connection open as long as possible.


### Prerequisites
* tor should be installed and to configured to open a SOCKS listener on some port.
* python **pysocks** package 

### Installing
1. Installing tor
```
sudo apt update && sudo apt install tor
```

2. Configure tor to open SOCKS5 proxy and restarting the service 
```
echo "SocksPort localhost:9050" | sudo tee -a /etc/tor/torrc && sudo systemctl restart tor
```

3. installing pysocks using pip:
```
pip3 install pysocks
```
*if you got "pip3 not found", try:*
```
sudo apt install python3-pip
```
and try step 3 again.

### Running
configure these variables and run hammer.py
Number of simoultanous connections :
```
THREADS = No_of_THREADS
```
Your target info: IP, PORT, HOSTNAME and the WEB_SERVER:
```
TARGET, TARGET_PORT, TARGET_HOST = '1.2.3.4', 80, 'example.com'
WEB_SERVER = "nginx"  # nginx or apache2
```
and run:
```
python hammer.py
```
