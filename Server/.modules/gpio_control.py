from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from gpiozero import LED

# Dictionary to map pin numbers to LED objects
leds = {}

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Extract request data
        content_length = int(self.headers['Content-Length'])
        data = self.rfile.read(content_length)
        payload = json.loads(data.decode('utf-8'))

        # Get pin number and state from the request data
        pin = payload.get('pin')
        state = payload.get('state')

        # Check if pin and state are provided
        if pin is None or state is None:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'Pin number and state must be provided'}).encode('utf-8'))
            return

        # Check if pin is valid (should be an integer)
        try:
            pin = int(pin)
        except ValueError:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'Invalid pin number'}).encode('utf-8'))
            return

        # Check if state is valid (should be a boolean)
        if not isinstance(state, bool):
            self.send_response(400)
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'Invalid state value'}).encode('utf-8'))
            return

        # Initialize LED object for the pin if not already created
        if pin not in leds:
            leds[pin] = LED(pin)

        # Set the state of the LED
        if state:
            leds[pin].on()
        else:
            leds[pin].off()

        # Send success response
        self.send_response(200)
        self.end_headers()
        self.wfile.write(json.dumps({'success': True}).encode('utf-8'))

def run_server():
    server_address = ('', 4000)
    httpd = HTTPServer(server_address, RequestHandler)
    print(f'Starting gpio-server on {server_address}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()

