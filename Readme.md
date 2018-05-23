# DE(CENTRALIZED)-TRAFFIC REGULATOR
	A Traffic marking web portal that allows verhicals to broadcast traffic situations live on Tangle. Using IOTA MAM module, the system will allow for emit and access encrypted data stream, like RSS, over the Tangle for any party to "subscribe" to the channel.


## Requirements
	Ubuntu 16.04
	Python 3+
	Virtualenv

## Instructions
1. Make sure "iotaproxy_npm" (see below) is setup accordingly and ready to run.
2. All requirements meet
3. Create a virtual environment for python3
4. From inside virtualenv, enter the source directory
5. Install the requirements.txt:
```
pip install -r requirements.txt
```
6. Start Django web server at custom port 7777:
```
python runserver manage.py localhost:7777
```

# iotaproxy
	A simple proxy server for the IOTA tangle network, supporting the attachToTangle command (PoW)
	source: https://github.com/TimSamshuijzen/iotaproxy

## Requirements
	Node.js

## Instructions
1. Enter the "iotaproxy_npm" directory:
```
cd iotaproxy_npm
```
2. Install the dependiences:
```
npm install
```
3. Edit index.js to set preferred connection to public iota node. For example:
```
iotaProxy.start(
  {
    host: 'http://node02.iotatoken.nl', // PUBLIC IOTA NODE, used to relay traffic to tangle.
    port: 14265,						// Port of PUBLIC NODE
    localPort: 14265,					// Listening on http://localhost for light node to send request to the proxy
    overrideAttachToTangle: true,		// Do the POW on proxy before replay to tangle because public node doesnot support for POW
    timeout: 15							// Time out in minutes
  }
);
```
4. Run the proxy server:
```
npm start
```

# Previews
The Web portal exists at http://localhost:7777

[!alt text](https://raw.githubusercontent.com/benuha/iota-pymessenger/)


# License
All projects licensed under the GNU General Public License (GPL) version 3.