from http.server import SimpleHTTPRequestHandler, HTTPServer
import json


class testHTTPServer_RequestHandler(SimpleHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin","*")
        self.send_header('Content-type', 'text/html')
        self.end_headers()
    
    def do_POST(self):
        print('*'*30)
        self._set_headers()
        print(self.headers['content-type'])
        self.data_string = self.rfile.read(int(self.headers['Content-Length']))
        self.send_response(200)
        self.end_headers()

        data = json.loads(self.data_string)
        print(data)

        ds = bytes('1,1,1,1','utf-8')
        self.wfile.write(ds)


def run():
    port = 8000
    print('starting server, port', port)

    # Server settings
    server_address = ('127.0.0.1', port)
    httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
    print('running server...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()