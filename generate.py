# check https://pypi.org/project/anytree/
# consider https://pythonhosted.org/watchdog/quickstart.html#a-simple-example

import markdown
import os
import pathlib
import re
import shutil
import sys

from PIL import Image
from PIL import ImageEnhance
from PIL.ImageOps import autocontrast
from PIL.ImageOps import fit

IN_FOLDER = 'in'
OUT_FOLDER = 'out'
WIDTH = 540
SHORT = 270
GUTTER = 32

SKIP_IMAGES = len(sys.argv) > 1 and sys.argv[1] == 'skip_images'

print('')
if SKIP_IMAGES:
	print('Skipping images\n')

def clean_path(path):
	return re.sub('\d+ - ', '', path)

def hero(func):
	def div(*args):
		return f'<div class="content-hero">{func(*args)}</div>'
	return div

def block(func):
	def div(*args):
		return f'<div class="block">{func(*args)}</div>'
	return div

def templetize_breadcrumbs(path):
	out = '<ul class="crumbs">'
	parts = ('Home', ) + path.parts
	for i, part in enumerate(parts):
		if i != len(parts) - 1:
			href = pathlib.Path('/', *parts[1:i+1], 'index.html')
			out += f'<li><a href="{href}"><span class="crumb">{part}</span></a></li>'
		else:
			out += f'<li>{part}</li>'
	out += '</li></ul>'
	return out

def templetize_header(text):
	return f'<h1 class="header">{text}</h1>'

def templetize_subheader(text):
	return f'<h2 class="subheader">{text}</h2>'

def templetize_markdown(file):
	with open(file, 'r') as fp:
		md = fp.read()
	return f'<div class="copy">{markdown.markdown(md)}</div>'

@hero
def templetize_hero_image(file):
	return f'<img src="{file} 2x" width="{2 * WIDTH + GUTTER}"/>'

@block
def templetize_image(file):
	return f'<img src="{file} 2x" width="{WIDTH}"/>'

@block
def templetize_vimeo(id):
	return f'<iframe src="https://player.vimeo.com/video/{id}?byline=0&portrait=0&title=0" width="{WIDTH}" height="{WIDTH}" frameborder="0" allow="autoplay; fullscreen" allowfullscreen></iframe>'

@block
def templetize_video(file):
	return f'<video width="{WIDTH}" controls><source src="{file}" type="video/mp4"></video>'

@block
def templetize_dir(infull, path, outfull):
	jpg_thumbpath = os.path.join(infull, '- thumb.jpg')
	png_thumbpath = os.path.join(infull, '- thumb.png')
	if os.path.isfile(jpg_thumbpath) or os.path.isfile(png_thumbpath):
		image = templetize_image(pathlib.Path(path, '- thumb.jpg'))
		outpath = pathlib.Path(outfull, '- thumb.jpg')
		deploy_resized(jpg_thumbpath if os.path.isfile(jpg_thumbpath) else png_thumbpath, outpath, True)
	else:
		image = ''
	return f'<a href="{pathlib.Path(path, "index.html")}"/>{image}<p>{path}</p></a>'

def deploy(inpath, outpath):
	outpath.parents[0].mkdir(parents=True, exist_ok=True)
	shutil.copyfile(inpath, outpath)

def deploy_resized(inpath, outpath, crop = False):
	if SKIP_IMAGES:
		return
	outpath.parents[0].mkdir(parents=True, exist_ok=True)
	outpath = outpath.with_suffix('.jpg')
	with Image.open(inpath) as image:
		image = image.convert("RGB")
		if crop:
			image = fit(image, (2 * WIDTH, WIDTH))
			image = image.convert("L")
			# enhancer = ImageEnhance.Brightness(image)
			# image = enhancer.enhance(2.0)
			# image = autocontrast(image)
		image.thumbnail((2 * WIDTH, 2 * WIDTH))
		image.save(str(outpath) + ' 2x', "JPEG")
		image.thumbnail((WIDTH, WIDTH))
		image.save(outpath, "JPEG")

def deploy_resized_hero(inpath, outpath):
	if SKIP_IMAGES:
		return
	outpath.parents[0].mkdir(parents=True, exist_ok=True)
	outpath = outpath.with_suffix('.jpg')
	with Image.open(inpath) as image:
		image = image.convert("RGB")
		size = 2 * WIDTH + GUTTER
		image.thumbnail((2 * size, 2 * size))
		image.save(str(outpath) + ' 2x', "JPEG")
		image.thumbnail((size, size))
		image.save(outpath, "JPEG")

# ****************************************************************************************** deploy assets
shutil.copytree(
	pathlib.Path(IN_FOLDER, '- assets'),
	pathlib.Path(OUT_FOLDER, 'assets'),
	dirs_exist_ok=True)

# ****************************************************************************************** parse folder
for root, dirs, files in os.walk(IN_FOLDER):

	if '.git' in root:
		continue

	outroot = pathlib.Path(clean_path(root)).relative_to(IN_FOLDER)
	outpath = pathlib.Path(OUT_FOLDER, outroot)

	items = dirs + files
	items.sort()

	# ****************************************************************************************** html
	doc = ['<html><meta name="viewport" content="width=device-width, initial-scale=.5">']

	rootpath = ""
	for _ in range(len(outroot.parts)):
		rootpath += '../'
	doc.append(f'<link rel="stylesheet" type="text/css" href="{rootpath}style.css">')
	doc.append(f'<link href="https://fonts.googleapis.com/css2?family=Podkova&family=Lato:wght@300&display=swap" rel="stylesheet">')
	doc.append('<body>')

	if len(outroot.parts) >= 1:
		doc.append(templetize_breadcrumbs(outroot))

	# ****************************************************************************************** content

	doc.append(f'<div class="content">')

	# ****************************************************************************************** header

	doc.append(f'<div class="content-first-cell">')
	
	headerpath = os.path.join(root, '- header.md')
	if os.path.isfile(headerpath):
		doc.append(templetize_markdown(headerpath))
	else:
		if len(outroot.parts) >= 1:	
			doc.append(templetize_header(outpath.name))

	infopath = os.path.join(root, '- info.md')
	if os.path.isfile(infopath):
		doc.append(templetize_markdown(infopath))
	
	doc.append('</div>')
	
	# print(dirs)
	# print(files)

	# ****************************************************************************************** items

	# state = ['']

	for item in items:

		if item[0] in ['.', '-']:
			continue

		cleaned = clean_path(item)
	
		itempath = pathlib.Path(cleaned)
		stem = itempath.stem
		suffix = itempath.suffix

		infull = pathlib.Path(root, item)
		outfull = pathlib.Path(outpath, cleaned)

		# if a file not a dir
		if item in files:

			# maybe state can just be a boolean, but starting with a stack just in case
			# if state[-1] == 'dir':
			# 	state.pop()
			# 	doc.append('</div>')

			if suffix == '.md':
				doc.append(templetize_markdown(infull))

			if suffix == '':
				doc.append(f'</div><div class="content content-latter">')  # start a new grid
				if len(stem) > 0:
					doc.append(templetize_subheader(stem))

			if suffix in ['.gif', '.jpg', '.jpeg', '.png']:
				if 'hero' in stem:
					doc.append(templetize_hero_image(itempath.with_suffix('.jpg')))
					deploy_resized_hero(infull, outfull)
				else:
					doc.append(templetize_image(itempath.with_suffix('.jpg')))
					deploy_resized(infull, outfull)

			if suffix == '.vimeo':
				doc.append(templetize_vimeo(stem))

			if suffix == '.mp4':
				doc.append(templetize_video(itempath))
				deploy(infull, outfull)

		else:

			# if state[-1] != 'dir':
			# 	state.append('dir')
			# 	doc.append('<div>')

			# make link
			doc.append(templetize_dir(infull, cleaned, outfull))

	# ****************************************************************************************** /items
	
	doc.append(f'</div>')  # content
	# ****************************************************************************************** /content

	doc.append('</body></html>')
	# ****************************************************************************************** /html

	html = ''.join(doc)

	outfile = pathlib.Path(outpath, 'index.html')

	# indent and print output file
	for _ in range(4 * len(outroot.parts)):
		print(' ', end = '')
	print(outfile)

	outpath.mkdir(parents=True, exist_ok=True)
	with outfile.open('w') as file:
		file.write(html)

print('')
