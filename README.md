# PIPAE Data Server

This is a Flask server that receives HTTP requests containing a JSON from the Network Server and processes the encrypted and compressed `payload` property.

## Installation & Running

Install the `pycryptodome` and `flask` packages with `pip` before running, since base64 is supported by default on Python.  

Once the requirements are installed, run it with `python decode.py`. The server is hosted on port 5000 by default.
