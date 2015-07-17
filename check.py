# -*- coding:utf-8 -*-

import os,sys
UI_RES_PATH = 'D:/H30/program/client/res/ui/'
UI_SCRIPT_PATH = 'D:/H30/program/client/script/'
png_2_plist_map = {}

plist_png_map = {}
scale9_png = []
all_used_png = []

alone_png = []
ignores = [
	'GUI',
    'publish/icon',
    'publish/icon/blood',
    'publish/icon/chat',
    'publish/icon/damage',
    'publish/icon/quest',
	'res/common/animation',
    'res/common/enlarge_jiugong'
]

TP = '"C:/Program Files (x86)/CodeAndWeb\TexturePacker/bin/TexturePacker.exe"'

def run_cmd(cmd_str):
	import subprocess
	print 'chenpeng exec---> ' + cmd_str
	output_file = sys.stdout
	p = subprocess.Popen(cmd_str, shell=True, stdout=output_file, stderr=output_file,env= os.environ)
	return p.wait()


def get_image_size(img_file):
	import Image
	img = Image.open(img_file)
	return max(img.size[0],img.size[1]),min(img.size[0],img.size[1])

def main():

	json_files = []
	for parent, dirs, files in os.walk(UI_RES_PATH):
		for fname in files:
			if fname.lower().endswith('.json'):
				json_files.append(os.path.join(parent, fname).replace('\\', '/'))


	for file in json_files:
		check_file(file)
		find_scale9_png(file)

	#check unused png

	# print all_used_png
	#
	# for parent, dirs, files in os.walk(UI_RES_PATH):
	# 	import shutil
	# 	for fname in files:
	# 		if fname.lower().endswith('.png'):
	# 			f_path = os.path.join(parent, fname).replace('\\', '/')
	# 			rel_path = f_path[len(UI_RES_PATH):]
	# 			if rel_path not in all_used_png:
	# 				print rel_path
	# 				shutil.copyfile( f_path, 'D:/tmp/' + rel_path.replace('/','_'))
	for parent, dirs, files in os.walk(UI_RES_PATH):
		import shutil
		number = 0
		tmp_dir = 'D:/tmp/ui/'
		parent = parent.replace('\\', '/')

		plist_file_base = os.path.join(parent, os.path.basename(parent)).replace('\\', '/')
		rel_dir = parent[len(UI_RES_PATH):]


		if rel_dir in ignores:
			continue
		print rel_dir
		pngs = []
		for fname in files:

			if fname.lower().endswith('.png'):

				f_path = os.path.join(parent, fname).replace('\\', '/')

				rel_path = f_path[len(UI_RES_PATH):]
				if os.path.exists( f_path[:-3] + 'plist') or os.path.exists( f_path[:-3] + 'fnt') or rel_path in scale9_png:
					continue
				width, height = get_image_size(f_path)
				if width > 1000 and height >= 500:
					alone_png.append(rel_path)
					continue
				if rel_dir in ('res/common/icon/item', 'publish/img'):

					to_file = os.path.join( tmp_dir, rel_path)
					dir_name = os.path.dirname(to_file)
					if not os.path.exists(dir_name):
						os.makedirs(dir_name)
					if os.path.exists(f_path):
						shutil.copyfile( f_path, to_file)
						os.remove(f_path)



					p_file = f_path[:-3] + 'plist'
					rel_plist = p_file[len(UI_RES_PATH):]
					cmd = "%s D:/tmp --format cocos2d --size-constraints NPOT --opt RGBA8888 --scale 1 --max-height 1024 --sheet %s --data %s"%\
			            ( TP, f_path, p_file)
					plist_png_map[rel_plist] = [rel_path]
					png_2_plist_map['ui/' +rel_path ] = rel_plist
					run_cmd(cmd)
					dir_path = tmp_dir +  parent[len(UI_RES_PATH):].split('/')[0]
					shutil.rmtree(dir_path)

					continue

				pngs.append('ui/' + rel_path)
				to_file = os.path.join( tmp_dir, rel_path)
				dir_name = os.path.dirname(to_file)
				if not os.path.exists(dir_name):
					os.makedirs(dir_name)
				if os.path.exists(f_path):
					shutil.copyfile( f_path, to_file)
					os.remove(f_path)
				number +=1
		if number > 0:

			print plist_file_base

			plist_file = plist_file_base+'.plist'
			png_file = plist_file_base+'.png'
			cmd = "%s D:/tmp --format cocos2d --size-constraints NPOT --opt RGBA8888 --scale 1 --max-height 1024 --sheet %s --data %s"%\
			      ( TP, png_file, plist_file)
			rel_plist = plist_file[len(UI_RES_PATH):]
			plist_png_map[rel_plist] = pngs
			for pngf in pngs:
				png_2_plist_map[pngf] = rel_plist
			run_cmd(cmd)
			dir_path = tmp_dir +  parent[len(UI_RES_PATH):].split('/')[0]
			shutil.rmtree(dir_path)
	for file in json_files:
		replace_file(file)

	# import shutil
	# for png_file in list(set(scale9_png)):
	# 	in_file = os.path.join( UI_RES_PATH, png_file)
	# 	to_file = os.path.join( 'D:/tmp/', png_file)
	# 	dir_name = os.path.dirname(to_file)
	# 	if not os.path.exists(dir_name):
	# 		os.makedirs(dir_name)
	# 	if os.path.exists(in_file):
	# 		shutil.copyfile( in_file, to_file)
	# 	else:
	# 		print in_file

	return 0



def find_scale9_png(file_name):
	json_file = open( file_name, 'r')
	flag = False
	path = None
	for line in json_file.readlines():
		if line.find('"classname": "ImageView"') >=0 or flag:
			flag =True
			if line.find('path') >=0 and line.find('png') >=0:
				path =  line.strip().split(':')[1].strip()[1:-2]
			if line.find('scale9Enable') >=0:
				if line.find('true')>=0 and path:
					scale9_png.append(path)
				flag = False
				path = None
	json_file.close()


def replace_file( file_name):
	json_file = open( file_name, 'r')
	index = 0
	txt_index = 0
	path = None
	lines = list(json_file.readlines())
	json_file.close()
	plists = []
	for idx, line in enumerate(lines):

		if line.find('texturesPng') >=0 or txt_index > 0:
			txt_index += 1
			if line.find('.png') >=0:
				pngf = 'ui/' + line.strip()[1:-2]
				if pngf in png_2_plist_map:
					plists.append(png_2_plist_map[pngf])
					lines[idx] = ''
					continue
			if line.find(']') >=0:
				txt_index = 0
		elif line.find('fileNameData') >=0 or \
			line.find('disabledData') >=0 or\
			line.find('normalData') >=0 or\
			line.find('pressedData') >=0 or\
			line.find('textureData') >=0 or\
			line.find('barFileNameData') >=0 or\
			line.find('ballPressedData') >=0 or\
			line.find('ballNormalData') >=0 or\
			line.find('ballDisabledData') >=0 or\
			line.find('progressBarData') >=0 or\
						index > 0:

			index +=1
			if index == 1:
				pass
			elif index == 2:
				if line.find('png') >=0:
					png_str = line.strip().split(':')[1].strip()
					png_file = 'ui/' + png_str.strip()[1:-2]

					if png_file in png_2_plist_map:
						plist_file = png_2_plist_map[png_file]
						if plist_file:
							path = plist_file
							lines[idx] = line.replace('"path": "', '"path": "ui/')

					print 'path', path

			elif index == 3:

				if path and line.find('.plist') == -1:
					lines[idx] = line.replace('"",', '"%s",'%path)
				else:
					path = None

			elif index == 4:
				if path:
					lines[idx] = line.replace('0','1')
				path = None
			else:
				index = 0
			print lines[idx], index
	plists= list(set(plists))
	out_file = open( file_name, 'w')
	for line in lines:

		if line.find('"textures":') >=0 :
			flag = False
			if line.find(']') >=0:
				flag = True
				out_file.write('  "textures": [\n')
			else:
				out_file.write(line)
			lens = len(plists)
			for idx in xrange(lens):
				pl = plists[idx]
				if idx == lens -1:
					out_file.write('  "%s"\n'%pl)
				else:
					out_file.write('  "%s",\n'%pl)
			if flag:
				out_file.write('  ],\n')
		else:
			out_file.write(line)
	out_file.close()
def check_file(file_name):

	json_file = open( file_name, 'r')
	index = 0
	path = None

	for line in json_file.readlines():
		if line.find('fileNameData') >=0 or \
			line.find('disabledData') >=0 or\
			line.find('normalData') >=0 or\
			line.find('pressedData') >=0 or\
			line.find('textureData') >=0 or\
			line.find('barFileNameData') >=0 or\
			line.find('ballPressedData') >=0 or\
			line.find('ballNormalData') >=0 or\
			line.find('ballDisabledData') >=0 or\
			line.find('progressBarData') >=0 or\
						index > 0:

			index +=1
			if index == 1:
				pass
			elif index == 2:
				if line.find('png') >=0:
					path = line.strip().split(':')[1].strip()

			elif index == 3:
				if path and line.find('plist') == -1:
					line = line.replace('"",', path)
					all_used_png.append( path.strip()[1:-2])
					plist = path.replace('png','plist')

			elif index == 4:
				if path:
					line = line.replace('0','1')
				path = None
			else:
				index = 0
			#print line

def test1():
	for parent, dirs, files in os.walk(UI_SCRIPT_PATH):
		for fname in files:
			fpath = os.path.join(parent, fname).replace('\\', '/')
			_fix(fpath)

def _fix(filename):
	if filename[len(UI_SCRIPT_PATH):].split('/')[0] in('helper', 'ui', 'visual_entities'):
		pass
	else:
		return
	ffile = open( filename, 'r')
	lines = ffile.readlines()
	ffile.close()
	cc = False
	have = False
	for line in lines:
		if line.find('as cconst') >=0:
			cc = True
		if line.find('cconst.') >=0:
			have =True
	if have and not cc:
		ffile = open( filename, 'w')
		for idx,line in enumerate(lines):
			ffile.write(line)
			if idx == 2:
				ffile.write('import client_const as cconst\r\n')



def _filter(filename):
	if filename[len(UI_SCRIPT_PATH):].split('/')[0] in('helper', 'ui', 'visual_entities'):
		pass
	else:
		return
	ffile = open( filename, 'r')
	lines = ffile.readlines()
	ffile.close()

	ffile = open( filename, 'w')
	for line in lines:
		if line.find('loadTexture') >=0:
			string = line.rstrip()
			string = string[:-1] + ',cconst.WIDGET_TEXTURERESTYPE)\r\n'
			ffile.write(string)
		else:
			ffile.write(line)
	ffile.close()
def test():
	for parent, dirs, files in os.walk(UI_RES_PATH):
		for fname in files:
			if fname.lower().endswith('.pkm') or fname.lower().endswith('.pvr') :
				os.remove(os.path.join(parent, fname).replace('\\', '/'))
	# for file_name in ('D:/H30/program/client/res/etc_hex.py','D:/H30/program/client/res/pvr_hex.py',):
	#
	# 	ffile = open( file_name, 'r')
	# 	lines = ffile.readlines()
	# 	ffile.close()
	#
	# 	ffile = open( file_name, 'w')
	# 	for line in lines:
	# 		if line.strip().startswith("'ui/res/combat_over"):
	# 			pass
	# 		else:
	# 			ffile.write(line)
	# 	ffile.close()

if __name__ == "__main__":
	test()
	main()
