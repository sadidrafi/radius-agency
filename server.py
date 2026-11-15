import os
import posixpath
import urllib.parse
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

PORT = 8080
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class CleanURLHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def _rewrite_path(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        clean = path.rstrip('/')
        
        if clean:
            rel = clean.lstrip('/')
            # Check directory index.html
            dir_index = os.path.join(DIRECTORY, rel, 'index.html')
            if os.path.isfile(dir_index):
                self.path = '/' + rel + '/index.html'
                if parsed.query:
                    self.path += '?' + parsed.query
                return
                
            # Check .html file
            html_file = os.path.join(DIRECTORY, rel + '.html')
            if os.path.isfile(html_file):
                self.path = '/' + rel + '.html'
                if parsed.query:
                    self.path += '?' + parsed.query
                return

    def do_GET(self):
        self._rewrite_path()
        return super().do_GET()

    def do_HEAD(self):
        self._rewrite_path()
        return super().do_HEAD()

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

def run():
    server_address = ('', PORT)
    httpd = ThreadingHTTPServer(server_address, CleanURLHandler)
    print(f"Serving at http://localhost:{PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()

if __name__ == '__main__':
    run()
