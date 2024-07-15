import json
import os
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

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

class DirectoryChangeHandler(FileSystemEventHandler):
	def __init__(self, callback):
		self.callback = callback
	
	def on_any_event(self, event):
		self.callback()

def run(port=8080):
	server_address = ('', port)
	httpd = HTTPServer(server_address, Server)
	print(f'Starting JSON server on port {port}...')
	httpd.serve_forever()

def monitor_directory(directory, callback):
	event_handler = DirectoryChangeHandler(callback)
	observer = Observer()
	observer.schedule(event_handler, directory, recursive=True)
	observer.start()
	try:
		while True:
			time.sleep(1)
	except KeyboardInterrupt:
		observer.stop()
	observer.join()

def start_server_thread():
	server_thread = threading.Thread(target=run)
	server_thread.daemon = True
	server_thread.start()
	return server_thread

server_thread = start_server_thread()

def restart_server():
	global server_thread
	if server_thread.is_alive():
		server_thread.join()
	server_thread = start_server_thread()
