python3 ./src/main.py

cd public && python3 -m http.server 8888


if self.path == "/favicon.ico":
    self.send_response(204)  # "No Content" status
    self.end_headers()
    return
    
    
