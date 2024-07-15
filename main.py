import webbrowser

from server import run

if __name__ == '__main__':
	PORT = 8080
	webbrowser.open_new(f'http://127.0.0.1:{PORT}')
	run(port=PORT)