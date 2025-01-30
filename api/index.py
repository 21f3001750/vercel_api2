import json
import os
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# Load data from JSON file
DATA_FILE = os.path.join(os.path.dirname(__file__), "data.json")
try:
    with open(DATA_FILE, "r") as file:
        data = json.load(file)
except Exception as e:
    data = []
    print(f"Error loading data: {e}")

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            parsed_path = urlparse(self.path)
            query_params = parse_qs(parsed_path.query)

            # Extract 'name' query params (always a list)
            requested_names = query_params.get("name", [])
            marks=[]
            for name in requested_names:
                if data['name'] ==name:
                    marks.append(data['marks'])


            # Extract marks for matching names
            # marks = [entry["marks"] for entry in data if entry["name"] in requested_names]

            response = {"marks": marks}

            # Send response headers
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            # Send response body
            self.wfile.write(json.dumps(response).encode("utf-8"))
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))

        
