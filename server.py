from http.server import SimpleHTTPRequestHandler, HTTPServer
import json


class testHTTPServer_RequestHandler(SimpleHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin","*")
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.flush_headers()
    
    def do_POST(self):
        print('*'*30)
        print(self.headers['content-type'])
        self.data_string = self.rfile.read(int(self.headers['Content-Length']))
        self._set_headers()

        data = json.loads(self.data_string)
        print(data)
        js_da = {"ana":"11"}
        js_du = json.dumps(js_da)
        print(js_du.encode())
        self.wfile.write(js_du.encode())
        return 

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