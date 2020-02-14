import math as m
import re
import fpdf as pdf

def generate_labels(data, label_shape=(7, 3), local=False, debug=0):
	num_inst = len(data)
	num_per_page = label_shape[0] * label_shape[1]
	num_pages = m.ceil(num_inst / num_per_page)

	class PDF(pdf.FPDF):
		def header(self):
			pass
		def footer(self):
			pass

	doc = PDF(format='A4')
	doc.set_auto_page_break(0)
	doc.set_margins(0, 0, 0)
	doc.add_font('def', '', 'FreeSans.ttf', uni=True)
	doc.set_font('def', '', 12)

	width, height = doc.w, doc.h
	cell_w, cell_h = width / label_shape[1], height / label_shape[0]
	delta_y = cell_h / 3

	#print(width, height)

	j = 0
	for i in range(num_inst):
		if i % num_per_page == 0:
			doc.add_page()
			j = 0
		elif i % label_shape[1] == 0:
			doc.ln()

		x = (j % label_shape[1]) * cell_w
		y = int(j / label_shape[1]) * cell_h
		j += 1

		if not data[i]:
			continue

		# Index.
		doc.set_xy(x,y)
		doc.set_font('def', '', 12)
		doc.cell(cell_w, delta_y, txt=data[i][0], border=debug, align='C')

		# Name Surname.
		y += delta_y
		doc.set_xy(x,y)
		doc.set_font('def', '', 13)
		doc.cell(cell_w, delta_y, txt=data[i][1] + ' ' + data[i][2], border=debug, align='C')

		# Voice.
		y += delta_y
		doc.set_xy(x,y)
		doc.set_font('def', '', 12)
		doc.cell(cell_w, delta_y, txt=data[i][3], border=debug, align='C')

	if local:
		print('Saving file locally to output.pdf.')
		return doc.output('./output.pdf', dest='F').encode('latin-1')
	else:
		return doc.output('./output.pdf', dest='S').encode('latin-1')
	

if __name__ == '__main__':
	import sys

	if len(sys.argv) < 2:
		print('Usage: generate_labels.py [data_file.tsv]')
		exit(1)

	indices = [0,1,2,3]
	data = []
	with open(sys.argv[1], 'r') as f:
		for l in f:
			if not l.strip():
				data.append([])
				continue
			words = re.split('[\t,]', l)
			parts = [words[i].strip() for i in indices]
			data.append(parts)

	generate_labels(data, local=True)

