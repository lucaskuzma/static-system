# check https://pypi.org/project/anytree/

import os
import re
import pathlib

IN_FOLDER = 'in'
OUT_FOLDER = 'out'

def templetize_header(title):
	return f'<h1>{title}<h1>'

def templetize_image(file):
	return f'<img src="{file}"/>'

def templetize_dir(root, dir):
	return f'<a href="{pathlib.Path(root, dir)}"/>{dir}</a>'

def clean_path(path):
	return re.sub('\d+ - ', '', path)

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
		itempath = pathlib.Path(item)
		filename = itempath.stem
		extension = itempath.suffix

		cleaned = clean_path(filename)
		
		# print(cleaned, extension)

		if item in files:

			if extension == '':
				doc.append(templetize_header(cleaned))

			if extension == '.gif':
				doc.append(templetize_image(cleaned + extension))

		else:

			# make link
			doc.append(templetize_dir(root, cleaned))

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


