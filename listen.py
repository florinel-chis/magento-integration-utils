import http.server
import socketserver
import json
import logging

# Configure logging
logging.basicConfig(filename='requests.log', level=logging.INFO, format='%(asctime)s - %(message)s')

class RequestHandler(http.server.BaseHTTPRequestHandler):
    def handle_request(self):
        # Log request headers and full URL
        logging.info("Method: %s", self.command)
        logging.info("Headers: %s", self.headers)
        logging.info("Requested URL: %s", self.path)

        # Read and log payload if present
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length > 0:
            payload = self.rfile.read(content_length)
            try:
                payload_data = json.loads(payload)
                logging.info("Payload (JSON): %s", json.dumps(payload_data, indent=2))
            except json.JSONDecodeError:
                logging.info("Payload (Text): %s", payload.decode('utf-8'))
        else:
            logging.info("No payload received.")

        # Send a generic response
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"{}")

    # Redirect all HTTP methods to the single handler
    do_GET = do_POST = do_PUT = do_DELETE = do_PATCH = do_OPTIONS = do_HEAD = handle_request

if __name__ == "__main__":
    PORT = 8080  # Change this to the desired port
    with socketserver.TCPServer(("", PORT), RequestHandler) as httpd:
        print(f"Serving on port {PORT}")
        httpd.serve_forever()
