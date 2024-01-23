import os
import http.server as server
import socketserver

def convert_image():
    pass
class HTTPRequestHandler(server.SimpleHTTPRequestHandler):
    """Extend SimpleHTTPRequestHandler to handle PUT requests"""
    def do_PUT(self):
        if self.headers["action"] == "TEST":
            print("no clue what to do :)")
            self.send_response(200, 'Done')
            self.end_headers()
        else:
            """Save a file following a HTTP PUT request"""

            # print("DATA: " + str(self.headers))
            # FileNotFoundError: [Errno 2] No such file or directory: ''
            filename = os.path.basename(self.path)
            print("Filename: " + str(os.path.basename(self.path)))

            # # Don't overwrite files
            # if os.path.exists(filename):
            #     self.send_response(409, 'Conflict')
            #     self.end_headers()
            #     reply_body = '"%s" already exists\n' % filename
            #     self.wfile.write(reply_body.encode('utf-8'))
            #     return

            file_length = int(self.headers['Content-Length'])
            with open(filename, 'wb') as output_file:
                output_file.write(self.rfile.read(file_length))
            self.send_response(201, 'Created')
            self.end_headers()
            reply_body = 'Saved "%s"\n' % filename
            self.wfile.write(reply_body.encode('utf-8'))
            convert_image()

# if __name__ == '__main__':
#     server.test(HandlerClass=HTTPRequestHandler)
with socketserver.TCPServer(("192.168.1.164", 8000), HTTPRequestHandler) as httpd:
    print("serving at port", 8000)
    httpd.serve_forever()