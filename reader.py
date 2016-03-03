import sys 
import os
import re

class ARFFreader :
	
	def __init__(self, filename) :
		f = open(filename, 'r')
		content = f.read()
		lines = content.split('\n')
		self.check_file(content.lower())
		index = 0
		#Extract relation
		for i in range(len(lines)) :
			l = lines[i].lower()
			if "@relation" in l :
				self.__relation = l.split(" ")[1]
				index += 1
				break
			index += 1
		self.__attributes = []
		self.__options = []
		pattern = re.compile("\{.+\}")
		#Extract attributes
		for i in range(index, len(lines)) :
			l = lines[i].lower()
			if "@data" in l :
				index += 1
				break
			if "@attribute" in l :
				info = l.split()
				options = []
				if "{" in l :
					match = re.search(pattern, l)
					options = l[match.start():].strip("{ }\t")
					options = options.split(",")
					for i in range(len(options)) :
						options[i] = options[i].strip(" '")
				else :
					options = info[2:]
				for j in range(len(info)) :
					info[j] = info[j].strip()
				#options.append("?")
				self.__attributes.append(info[1])
				self.__options.append(options)
			index += 1
		self.__data = []
		print(self.__options[-1:])
		#Extract data
		for i in range(index, len(lines)) :
			l = lines[i].lower()
			if len(l) == 0 :
				continue
			if "@" in l or '%' in l :
				continue
			#info = l.replace(",", " ")
			#info = info.replace("\t", " ")
			info = l.split(",")
			data = []
			for j in range(len(info)) :
				k = info[j].strip("' ")
				if "real" in self.__options[j] :
					data.append(float(k))
					continue
				data.append(self.__options[j].index(k))
			self.__data.append(data)
		

	def check_file(self, content) :
		if not ("@relation" in content and "@attribute" in content
			and "@data" in content) :
			print("Error: file format")
			print("file should be of structure")
			print("@relation")
			print("@attribute")
			print("@data")
			exit()



	def relation(self) :
		return self.__relation

	def attributes(self) :
		return self.__attributes
    
	def options(self):
		return self.__options

	def data(self) :
		return self.__data
