import sys 
import os

class ARFFreader :
	
	def __init__(self, filename) :
		f = open(filename, 'r')
		content = f.read()
		lines = content.split('\n')
		self.check_file(content)
		index = 0
		#Extract relation
		for i in range(len(lines)) :
			l = lines[i]
			if "@relation" in l :
				self.__relation = l.split(" ")[1]
				index += 1
				break
			index += 1
		self.__attributes = {}
		#Extract attributes
		for i in range(index, len(lines)) :
			l = lines[i]
			if "@data" in l :
				index += 1
				break
			if "@attribute" in l :
				info = l.replace(",", "")
				info = info.replace("{", "")
				info = info.replace("}", "")
				info = info.split()
				for j in range(len(info)) :
					info[j] = info[j].strip()
				self.__attributes[info[1]] = info[2:]
			index += 1
		self.__data = []
		#Extract data
		for i in range(index, len(lines)) :
			print(l)
			l = lines[i]
			if len(l) == 0 :
				continue
			if "@" in l or '%' in l :
				continue
			data = l.split(",")
			for j in range(len(data)) :
				data[j] = data[j].strip()
			self.__data.append(data)
		

	def check_file(self, content) :
		if not ("@relation" in content and "@attribute" in content
			and "@data" in content) :
			print("Error: file format")
			print("file should be of structure")
			print("@relation")
			print("@attribute")
			print("@data")



	def relation(self) :
		return self.__relation

	def attributes(self) :
		return self.__attributes

	def data(self) :
		return self.__data
