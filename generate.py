# check https://pypi.org/project/anytree/

import os
from os.path import join, getsize
import re

def templetize_header(title):
	return f'<h1>{title}<h1>'

def templetize_image(file):
	return f'<img src="{file}"/>'

def templetize_dir(root, dir):
	return f'<a href="{os.path.join(root, dir)}"/>{dir}</a>'

def clean_path(path):
	return re.sub('\d+ - ', '', path)

for root, dirs, files in os.walk('in'):
    # print(root, "consumes", end=" ")
    # print(sum(getsize(join(root, name)) for name in files), end=" ")
    # print("bytes in", len(files), "non-directory files")

	# for dir in dirs: print(dir)
	# print('--')
	# print(clean_path(root))
	# continue

	doc = ['<body>']

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

		filename, extension = os.path.splitext(item)
		cleaned = clean_path(filename)
		
		# print(cleaned, extension)

		if item in files:

			if extension == '':
				doc.append(templetize_header(cleaned))

			if extension == '.gif':
				doc.append(templetize_image(cleaned + extension))

		else:

			doc.append(templetize_dir(root, cleaned))

	# indent
	for _ in range(4 * root.count('/')):
		print(' ', end = '')

	doc.append('</body>')

	html = ''.join(doc)
	# print(html)

	outpath = clean_path(root).replace('in', 'out', 1)
	outfile = os.path.join(outpath, 'index.html')

	print(outfile)

	os.makedirs(os.path.dirname(outfile), exist_ok=True)
	with open(outfile, 'w') as file:
		file.write(html)
