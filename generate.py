# check https://pypi.org/project/anytree/
# consider https://pythonhosted.org/watchdog/quickstart.html#a-simple-example

import os
import re
import pathlib
import shutil

IN_FOLDER = 'in'
OUT_FOLDER = 'out'

def clean_path(path):
	return re.sub('\d+ - ', '', path)

def templetize_breadcrumbs(path):
	out = '<ul>'
	parts = ('Home', ) + path.parts
	for i, part in enumerate(parts):
		if i != len(parts) - 1:
			href = pathlib.Path('/', *parts[1:i+1], 'index.html')
			out += f'<li><a href="{href}">{part}<a></li>'
		else:
			out += f'<li>{part}</li>'
	out += '</li>'
	return out

def templetize_header(text):
	return f'<h2>{text}<h2>'

def templetize_image(file):
	return f'<img src="{file}"/>'

def templetize_dir(path):
	return f'<a href="{pathlib.Path(path, "index.html")}"/>{path}</a>'

def deploy(inpath, outpath):
	shutil.copyfile(inpath, outpath)

for root, dirs, files in os.walk(IN_FOLDER):

	outroot = pathlib.Path(clean_path(root)).relative_to(IN_FOLDER)
	outpath = pathlib.Path(OUT_FOLDER, outroot)

	doc = ['<body>']

	doc.append(templetize_breadcrumbs(outroot))

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
				doc.append(templetize_header(stem))

			if suffix == '.gif' or suffix == '.jpg':
				doc.append(templetize_image(cleaned))
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


