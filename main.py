import webbrowser

from server import *

if __name__ == '__main__':
	PORT = 8080
	webbrowser.open_new(f'http://127.0.0.1:{PORT}')
	try:
		monitor_directory("data", restart_server)
	except KeyboardInterrupt:
		exit(0)