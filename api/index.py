import json
import os
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# Load data from the JSON file
DATA_FILE = os.path.join(os.path.dirname(__file__), "data.json")
with open(DATA_FILE, "r") as file:
    data = json.load(file)

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)
        
        names = query_params.get("name", [])  # Get list of names from query
        marks = [entry["marks"] for entry in data if entry["name"] in names]

        response = {"marks": marks}

        # Send response headers
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        # Send response body
        self.wfile.write(json.dumps(response).encode("utf-8"))
