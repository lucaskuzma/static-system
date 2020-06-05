# check https://pypi.org/project/anytree/
# consider https://pythonhosted.org/watchdog/quickstart.html#a-simple-example

import os
import pathlib
import re
import shutil

from PIL import Image

IN_FOLDER = 'in'
OUT_FOLDER = 'out'

def clean_path(path):
	return re.sub('\d+ - ', '', path)

def block(func):
	def div(*args):
		return f'<div class="block">{func(*args)}</div>'
	return div

def templetize_breadcrumbs(path):
	out = '<ul>'
	parts = ('Home', ) + path.parts
	for i, part in enumerate(parts):
		if i != len(parts) - 1:
			href = pathlib.Path('/', *parts[1:i+1], 'index.html')
			out += f'<li><a href="{href}">{part}</a></li>'
		else:
			out += f'<li>{part}</li>'
	out += '</li>'
	return out

def templetize_header(text):
	return f'<h1>{text}</h1>'

def templetize_subheader(text):
	return f'<h2>{text}<h2>'

@block
def templetize_image(file):
	return f'<img src="{file} 2x" width="540"/>'

@block
def templetize_vimeo(id):
	return f'<iframe src="https://player.vimeo.com/video/{id}?byline=0&portrait=0&title=0" width="540" height="540" frameborder="0" allow="autoplay; fullscreen" allowfullscreen></iframe>'

@block
def templetize_video(file):
	return f'<video width="320" height="240" controls><source src="{file}" type="video/mp4"></video>'

@block
def templetize_dir(path):
	return f'<a href="{pathlib.Path(path, "index.html")}"/>{path}</a>'

def deploy(inpath, outpath):
	outpath.parents[0].mkdir(parents=True, exist_ok=True)
	shutil.copyfile(inpath, outpath)

def deploy_resized(inpath, outpath):
	outpath.parents[0].mkdir(parents=True, exist_ok=True)
	outpath = outpath.with_suffix('.jpg')
	with Image.open(inpath) as image:
		image = image.convert("RGB")
		image.thumbnail((1080, 1080))
		image.save(str(outpath) + ' 2x', "JPEG")
		image.thumbnail((540, 540))
		image.save(outpath, "JPEG")

for root, dirs, files in os.walk(IN_FOLDER):

	outroot = pathlib.Path(clean_path(root)).relative_to(IN_FOLDER)
	outpath = pathlib.Path(OUT_FOLDER, outroot)

	doc = ['<body>']

	rootpath = ""
	for _ in range(len(outroot.parts)):
		rootpath += '../'
	doc.append(f'<link rel="stylesheet" type="text/css" href="{rootpath}style.css">')
	doc.append(f'<link href="https://fonts.googleapis.com/css2?family=Podkova&display=swap" rel="stylesheet">')

	doc.append(templetize_breadcrumbs(outroot))

	doc.append(templetize_header(outpath.name))

	# print(dirs)
	# print(files)

	items = dirs + files
	items.sort()

	for item in items:

		if item[0] == '.':
			continue

		cleaned = clean_path(item)
	
		itempath = pathlib.Path(cleaned)
		stem = itempath.stem
		suffix = itempath.suffix

		infull = pathlib.Path(root, item)
		outfull = pathlib.Path(outpath, cleaned)

		if item in files:

			if suffix == '':
				doc.append(templetize_subheader(stem))

			if suffix in ['.gif', '.jpg', '.jpeg', '.png']:
				doc.append(templetize_image(cleaned))
				deploy_resized(infull, outfull)

			if suffix == '.vimeo':
				doc.append(templetize_vimeo(stem))

			if suffix == '.mp4':
				doc.append(templetize_video(cleaned))
				deploy(infull, outfull)

		else:

			# make link
			doc.append(templetize_dir(cleaned))

	doc.append('</body>')

	html = ''.join(doc)

	outfile = pathlib.Path(outpath, 'index.html')

	# indent and print output file
	for _ in range(4 * len(outroot.parts)):
		print(' ', end = '')
	print(outfile)

	outpath.mkdir(parents=True, exist_ok=True)
	with outfile.open('w') as file:
		file.write(html)


