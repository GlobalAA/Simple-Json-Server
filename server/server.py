import json
from http.server import BaseHTTPRequestHandler, HTTPServer

from .content import Content


class Server(BaseHTTPRequestHandler):
	def _send_response(self, response, status=200):
		self.send_response(status)		
		self.send_header('Content-type', 'application/json')
		self.end_headers()
		self.wfile.write(json.dumps(response).encode('utf-8'))


	def do_GET(self):
		if self.path == "/":
			self.path = "/hello.json"

		content, status_code = Content(self.path, self.path == "/hello.json").parse_content()
		self._send_response(content, status_code)


def run(server_class=HTTPServer, handler_class=Server, port=8080):
	server_address = ('', port)
	httpd = server_class(server_address, handler_class)
	print(f'Starting JSON server on port {port}...')
	httpd.serve_forever()