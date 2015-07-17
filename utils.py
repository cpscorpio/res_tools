# -*- coding:utf-8 -*-

def get_dict_string( data, index =0):
	string = '{\n'
	for key, val in data.iteritems():
		string += '\t' * index + "'%s' : %s,\n"%(key,get_list_string(val,1))
	string += '}\n'
	print string
	return string

def get_list_string( data, index =0):
	string = '[\n'
	data = list(set(data))
	for item in data:
		if isinstance(item,list):
			string += '\t' * (index+1) + "%s,\n"%( get_list_string(item, index + 1))
		else:
			string += '\t' * (index+1) + "'%s',\n"%( str(item))
	string += '\t' * index +']'
	# print string
	return string