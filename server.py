from http.server import BaseHTTPRequestHandler, HTTPServer
from os import path
from urllib.parse import urlparse
import cgi
import io
curdir = path.dirname(path.realpath(__file__))
sep = '/'

# MIME-TYPE
mimedic = [
                        ('.html', 'text/html'),
                        ('.htm', 'text/html'),
                        ('.js', 'application/javascript'),
                        ('.css', 'text/css'),
                        ('.json', 'application/json'),
                        ('.png', 'image/png'),
                        ('.jpg', 'image/jpeg'),
                        ('.gif', 'image/gif'),
                        ('.txt', 'text/plain'),
                        ('.avi', 'video/x-msvideo'),
                    ]

class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):
    # GET
    # def do_GET(self):
    #     sendReply = False
    #     querypath = urlparse(self.path)
    #     filepath, query = querypath.path, querypath.query
        
    #     if filepath.endswith('/'):
    #         filepath += 'index.html'
    #     filename, fileext = path.splitext(filepath)
    #     for e in mimedic:
    #         if e[0] == fileext:
    #             mimetype = e[1]
    #             sendReply = True

    #     if sendReply == True:
    #         try:
    #             with open(path.realpath(curdir + sep + filepath),'rb') as f:
    #                 content = f.read()
    #                 self.send_response(200)
    #                 self.send_header('Content-type',mimetype)
    #                 self.end_headers()
    #                 self.wfile.write(content)
    #         except IOError:
    #             self.send_error(404,'File Not Found: %s' % self.path)

    # def do_POST(self) :
	   #  ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
	   #  print('aaa')
	   #  if ctype == 'multipart/form-data':
	   #      postvars = cgi.parse_multipart(self.rfile, pdict)
	   #  elif ctype == 'application/x-www-form-urlencoded':
	   #      length = int(self.headers.getheader('content-length'))
	   #      postvars = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)
	   #  else:
	   #      postvars = {}
    def do_POST(self):
        # Parse the form data posted
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={
                'REQUEST_METHOD': 'POST',
                'CONTENT_TYPE': self.headers['Content-Type'],
            }
        )

        # Begin the response
        self.send_response(200)
        self.send_header('Content-Type',
                         'text/plain; charset=utf-8')
        self.end_headers()

        out = io.TextIOWrapper(
            self.wfile,
            encoding='utf-8',
            line_buffering=False,
            write_through=True,
        )
        print('-jhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh')
        out.write('Client: {}\n'.format(self.client_address))
        out.write('User-agent: {}\n'.format(
            self.headers['user-agent']))
        out.write('Path: {}\n'.format(self.path))
        out.write('Form data:\n')

        # Echo back information about what was posted in the form
        for field in form.keys():
            field_item = form[field]
            print(field_item)
            if field_item.filename:
                # The field contains an uploaded file
                file_data = field_item.file.read()
                file_len = len(file_data)
                del file_data
                out.write(
                    '\tUploaded {} as {!r} ({} bytes)\n'.format(
                        field, field_item.filename, file_len)
                )
            else:
                # Regular form value
                out.write('\t{}={}\n'.format(
                    field, form[field].value))

        # Disconnect our encoding wrapper from the underlying
        # buffer so that deleting the wrapper doesn't close
        # the socket, which is still being used by the server.
        out.detach()

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