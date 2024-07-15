import json
import os
from dataclasses import dataclass

from . import config


@dataclass
class Content:
	url: str
	hello: bool
	
	def parse_content(self):
		self.path = f"{config.JSON_DIR}{self.url}"
		ext = self.path.split(".")[-1]
		
		if self.hello:
			return config.HELLO_DICT, 200
		
		if os.path.exists(self.path):
			if ext == "json":
				with open(self.path, 'r') as content:
					try:
						data = json.load(content)
						content.close()
						return data, 200
					except Exception as ex:
						return {"message": "File error", "error": str(ex)}, 502
			if ext == "html":
				with open(self.path, 'rb') as content:
					data = content.read()
					content.close()
					return data, 200
			else:
				raise Exception(f"Error open file on path {self.path}")
		else:
			if ext == "json":
				return {"message": "File not found"}, 404
			else:
				raise Exception(f"Error open file on path {self.path}")