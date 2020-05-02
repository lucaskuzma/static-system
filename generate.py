# check https://pypi.org/project/anytree/
# consider https://pythonhosted.org/watchdog/quickstart.html#a-simple-example

import os
import re
import pathlib

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

for root, dirs, files in os.walk(IN_FOLDER):
    # print(root, "consumes", end=" ")
    # print(sum(getsize(join(root, name)) for name in files), end=" ")
    # print("bytes in", len(files), "non-directory files")

	# for dir in dirs: print(dir)
	# print('--')
	# print(clean_path(root))
	# continue

	root = pathlib.Path(clean_path(root)).relative_to(IN_FOLDER)

	doc = ['<body>']

	doc.append(templetize_breadcrumbs(root))

	# print(dirs)
	# print(files)

	items = dirs + files
	items.sort()

	for item in items:

		if item[0] == '.':
			continue

		# print(file, end=" ")	
		# print(root, end=" ")
		# print(os.path.join(root, file))

		# filename, extension = os.path.splitext(item)
		itempath = pathlib.Path(clean_path(item))
		stem = itempath.stem
		suffix = itempath.suffix

		# print(cleaned, extension)

		if item in files:

			if suffix == '':
				doc.append(templetize_header(stem))

			if suffix == '.gif':
				doc.append(templetize_image(itempath))

		else:

			# make link
			doc.append(templetize_dir(itempath))

	# indent
	for _ in range(4 * len(root.parts)):
		print(' ', end = '')

	doc.append('</body>')

	html = ''.join(doc)
	# print(html)

	outpath = pathlib.Path(OUT_FOLDER, root)
	outfile = pathlib.Path(OUT_FOLDER, root, 'index.html')

	print(outfile)

	# os.makedirs(os.path.dirname(outfile), exist_ok=True)
	# with open(outfile, 'w') as file:
	# 	file.write(html)

	outpath.mkdir(parents=True, exist_ok=True)
	with outfile.open('w') as file:
		file.write(html)


