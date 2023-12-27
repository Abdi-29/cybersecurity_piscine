import argparse
import requests
from bs4 import BeautifulSoup
import re
import os

class Spider:
	def __init__(self, url, depth=5, path='./data/'):
		self.url = url
		self.depth = depth
		self.path = path
		if not os.path.isdir(path):
			os.mkdir(path)

	def download_image(self, current_depth=0):
		if current_depth > self.depth:
			return
		
		try:
			response = requests.get(self.url)
		except:
			print("lolol")
			exit(0)	
		if response.status_code != 200:
			return
		print(self.url)
		soup = BeautifulSoup(response.text, "html.parser")
		img_tag = soup.find_all("img")
		urls = [img['src'] for img in img_tag]
		for url in urls:
			filename = re.search(r'/([\w_-]+[.](jpg|jpeg|png|gif|bmp))$', url)
			if not filename:
				continue
			with open(f"{self.path}/{filename.group(1)}", 'wb') as f:
				if "http" not in url:
					url = '{}{}'.format(self.url, url)
				response = requests.get(url)
				f.write(response.content)	
			print(filename.groups(1))

			if current_depth < self.depth:
				for link_tag in soup.find_all('a', href=True):
					link_url = link_tag['href']
					if link_url.startswith('http'):
						self.url = link_url
						self.download_image(current_depth + 1)

parser = argparse.ArgumentParser(description="Spider Program for Downloading Images")
parser.add_argument("url", help="URL of the website")
parser.add_argument("-r", "--recursive", action="store_true", help="Recursively download images")
parser.add_argument("-l", "--depth", type=int, default=5, help="Maximum depth level for recursive download")
parser.add_argument("-p", "--path", default="./data/", help="Path where downloaded files will be saved")

args = parser.parse_args()

spider = Spider(args.url, args.depth, args.path)
if args.recursive:
	spider.download_image()
else:	
	spider.download_image(current_depth=0)