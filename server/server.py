import os
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import logging

# Set the path for logs folder to the current working directory (ensure it creates in the server folder)
log_directory = os.path.join(os.path.dirname(__file__), 'logs')
os.makedirs(log_directory, exist_ok=True)  # Create logs folder in the server directory

# Basic logging setup
logging.basicConfig(
    filename='logs/server.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)

# Load environment variables or use defaults
SERVER_HOST = os.getenv("SERVER_HOST", "127.0.0.1")
SERVER_PORT = int(os.getenv("SERVER_PORT", 8000))


def calculate_weight(text):
    """
    Calculates the weight of the given string based on specific rules:
    - If the string contains "aa" (case-insensitive), return 1000.
    - Otherwise, calculate based on:
        (1.5 * number of letters + 2 * number of digits) / number of spaces.
    """
    if "aa" in text.lower():
        logging.warning(f"Rule triggered: double 'a' detected >> {text.strip()}")
        return 1000

    letters = sum(1 for c in text if c.isalpha())
    digits = sum(1 for c in text if c.isdigit())
    spaces = text.count(' ')

    if spaces == 0:
        return 0

    weight = (1.5 * letters + 2 * digits) / spaces
    return weight


class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != "/calculate/":
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")
            return

        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)

        try:
            data = json.loads(body.decode())
            text = data.get("text", "")
            weight = calculate_weight(text)
            response = json.dumps({"weight": weight}).encode()

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(response)))
            self.end_headers()
            self.wfile.write(response)

            logging.info(f"Processed: '{text[:30]}...' => weight: {weight}")

        except Exception as e:
            logging.error(f"Error handling request: {e}")
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b"Internal Server Error")


def run_server():
    server_address = (SERVER_HOST, SERVER_PORT)
    httpd = HTTPServer(server_address, RequestHandler)
    logging.info(f"Server starting on {SERVER_HOST}:{SERVER_PORT}")
    httpd.serve_forever()


if __name__ == "__main__":
    run_server()
