# -*- coding:utf-8 -*-


import os
CCSPROJS_PATH = 'D:/H30/cocosStudio/CocosStudio/ccsprojs'
ASSSETS_PATH = 'D:/H30/cocosStudio/CocosStudio/assets'



json_pngs = {}
png_jsons = {}

def main():
	json_files = []
	for parent, dirs, files in os.walk(CCSPROJS_PATH):
		for fname in files:
			if fname.lower().endswith('.json'):
				json_files.append(os.path.join(parent, fname).replace('\\', '/'))


	for file in json_files:
		check_file(file)

	import utils
	jpf = open('json_pngs','w')
	jpf.write(utils.get_dict_string(json_pngs))
	jpf.close()

	pf = open('png_jsons','w')
	pf.write(utils.get_dict_string(png_jsons))
	pf.close()



def check_file(file_name):

	json_file = open( file_name, 'r')
	index = 0
	path = None
	json_pngs[file_name] = []
	for line in json_file.readlines():
		if line.find('fileNameData') >=0 or \
			line.find('disabledData') >=0 or\
			line.find('normalData') >=0 or\
			line.find('pressedData') >=0 or\
						index > 0:

			index +=1
			if index == 1:
				pass
			elif index == 2:
				if line.find('png') >=0:

					png_file = line.strip().split(':')[1].strip()
					rel_path = png_file.strip()[1:-2]
					json_pngs[file_name].append(rel_path)
					if rel_path.startswith('res/common'):

						png_json = png_jsons.get(rel_path,[])
						png_json.append(file_name)
						png_jsons[rel_path] = png_json

						path =  png_file.replace('png','plist')

			elif index == 3:
				if path and line.find('plist') == -1:
					line = line.replace('"",', path)
			elif index == 4:
				if path:
					line = line.replace('0','1')
				path = None
			else:
				index = 0
			#print line
if __name__ == "__main__":

	exit(main())
