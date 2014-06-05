#coding=utf-8
def lines(file):
	for line in file: yield line     #每次返回文件中的一行
	yield '\n'                     #在文件的结尾添加一个空行，让程序顺利结束

def blocks(file):
	"""
	程序主要用来收集文本中的块，然后利用各种办法把这一个块加上HTML标记，这个函数的主要用途就是
	收集程序的每一个块，提供给程序做相应的处理
	"""
	block = []
	for line in lines(file):            #依次遍历文件中的每一行
		if line.strip():                #如果不是空行，那么就要添加到数组里，这也就是收集块的过程 
			block.append(line)
		elif block:									#如果是空行，那么就要把当前收集的是一个块的字符串全都添加到一个数组里面返回，并且把数组清空
			yield ''.join(block).strip()
			block = [];

