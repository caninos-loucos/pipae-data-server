from flask import Flask, request, Response
import logging
import base64
import lz4.frame
from Crypto.Cipher import AES
app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)
@app.route('/', methods=['POST'])
def upload():
	data = request.get_json()
	
	if not data or 'params' not in data:
		return Response("Missing 'params' field", status=200)

	params = data['params']

	if 'payload' not in params:
		return Response("Missing 'payload' in params", status=400)

	payload = params['payload']

	key = b'00000000000000000000000000000000' 
	app.logger.debug(f"key = {key}")
	cipher = AES.new(key, AES.MODE_CTR)

	try:
		encrypted_data = base64.b64decode(payload)
	except Exception as e:
		app.logger.error(f"Decoding failed: {e}")
		return Response("Invalid base64 string", status=400)
	try:
	    	decrypted_data = cipher.decrypt(encrypted_data)
	except Exception as e:
		app.logger.error(f"Decrypting failed: {e}")
		return Response("Invalid string", status=400)

	app.logger.debug(f'Received byte data: {encrypted_data.hex()} with length {len(encrypted_data)}')

	try:
    		decompressed = lz4.frame.decompress(encrypted_data)
	except Exception as e:
		app.logger.error(f"{e}")
		return Response("Decompression error", status=400)

	app.logger.debug(f'Decompressed data: {decompressed.hex()}')

	return Response("Upload successful", status=200)

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=5000)
