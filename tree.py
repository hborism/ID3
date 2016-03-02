import os
import sys
import math
import copy

class Tree:
	__data=[]
	__no_examples=0
	__attributes=[]
	__options=[]
	__goal=""
	__goal_pos=0
	__goal_entropy=-1
	__root=0


	def __init__(self,data, attributes,options,goal):
		self.__data=data
		self.__attributes=attributes
		self.__options=options
		self.__goal=goal


		#find the goal_entorpy
		#x is the position of the goal attribute in self.data
		self.__goal_pos=attributes.index(goal)

		#p is the number of positive outcomes of the goal function in our examples
		p=0
		self.__no_examples=len(data)
		for i in range(self.__no_examples):
			p += data[i][self.__goal_pos]

		# entropy of goal
		self.__goal_entropy=self.entropy(p/self.__no_examples)

	def entropy(self, q):
		if q<=0 or q>=1:
			return 0
		return -(q*math.log(q,2)+(1-q)*math.log(1-q,2))

	def getRoot(self):
		return self.__root

	def getAttributes(self):
		return self.__attributes

	def goalEntropy(self):
		return self.__goal_entropy

	def gain(self, attribute, sorted_examples):
		if attribute not in self.__attributes:
			return -1

		#find position of attribute
		attribute_pos=0
		while self.__attributes[attribute_pos]!=attribute:
			attribute_pos+=1

		#calculate the number of examples
		no_examples=len(sorted_examples[0])+len(sorted_examples[1])
		if no_examples==0:
			return 0

		#creating a tree for this attribute (look at fig 18.4 in book)
		no_options=len(self.__options[attribute_pos])
		result=[]
		for c in range(0,no_options):
			result.append([0,0])

		for outcome in sorted_examples:
			for i in range(0, len(outcome)):
				result[outcome[i][attribute_pos]][outcome[i][self.__goal_pos]]+=1


		#calculate the remainder
		remainder=0
		c=0
		for c in range(0, no_options):
			if sum(result[c])!=0:
				remainder+=(sum(result[c])/no_examples)*(self.entropy(result[c][0]/sum(result[c])))


		#return goal entropy minus the remainder (see page 704 in book)
		return self.__goal_entropy-remainder


	def sortExamples(self,examples):
		sorted_examples=[]
		p_examples=[]
		n_examples=[]
		for i in range(0, len(examples)):
			if examples[i][self.__goal_pos]==0:
				p_examples.append(examples[i])
			else:
				n_examples.append(examples[i])

		sorted_examples.append(p_examples)
		sorted_examples.append(n_examples)

		return sorted_examples

	def importance(self, attributes, examples):
		maxgain=-1
		maxgain_attribute=""
		for x in attributes:
			gain=self.gain(x, examples)
			if gain>maxgain:
				maxgain=gain
				maxgain_attribute=x
		return maxgain_attribute

	def buildTree(self):
		attributes=copy.copy(self.__attributes)
		attributes.remove(self.__goal)

		attribute=self.importance(attributes,self.sortExamples(self.__data))
		options=self.__options[self.__attributes.index(attribute)]

		#create root node
		self.__root=Node(attribute,self.sortExamples(self.__data),options, "", "")

		self.populateTree(self.__root)


	def populateTree(self, parentNode):
		options=parentNode.getOptions()
		sorted_examples=parentNode.getSortedExamples()
		attribute_pos=self.__attributes.index(parentNode.getAttribute())
		sorted_examples_per_option=[]
		indent = parentNode.getIndent() + "\t"

		for op in range(0,len(options)):
			temp_examples=[]
			for outcome in sorted_examples:
				for example in outcome:
					if example[attribute_pos]==op:
						temp_examples.append(example)

			temp_examples=self.sortExamples(temp_examples)
			sorted_examples_per_option.append(temp_examples)
		#check that it works by printing. it produces the examples sorted as in figure 18.4
		#print(sorted_examples_per_option)

		#walk through each option to see if a child shall be a leaf or node
		for op in range(len(options)):
			option = options[op]
			if len(sorted_examples_per_option[op][0])==0 and len(sorted_examples_per_option[op][1])==0:
				focusNode=Node("Yes/no",[],[], indent, option)
				parentNode.addChild(focusNode)
			elif len(sorted_examples_per_option[op][0])==0:
				focusNode=Node("No",sorted_examples_per_option[op],[], indent, option)
				parentNode.addChild(copy.copy(focusNode))
			elif len(sorted_examples_per_option[op][1])==0:
				focusNode=Node("Yes",sorted_examples_per_option[op],[], indent, option)
				parentNode.addChild(focusNode)
			else:
				attributes=copy.copy(self.__attributes)
				attributes.remove(parentNode.getAttribute())
				attributes.remove(self.__goal)
				child_attribute=self.importance(attributes,sorted_examples_per_option[op])
				child_attribute_pos=self.__attributes.index(child_attribute)
				child_options=self.__options[child_attribute_pos]
				focusNode=Node(child_attribute,sorted_examples_per_option[op],child_options, indent, option)
				parentNode.addChild(focusNode)

				#recursion
				self.populateTree(focusNode)


class Node:

	def __init__(self, attribute, examples, options, indent, suffix):
		self.__attribute=attribute
		self.__sorted_examples=examples
		self.__options=options
		self.__children=[]
		self.__indent = indent
		self.__suffix = suffix

	def getIndent(self):
		return self.__indent

	def getAttribute(self):
		return self.__attribute

	def getSortedExamples(self):
		return self.__sorted_examples

	def getOptions(self):
		return self.__options

	def getChildren(self):
		return self.__children

	def addChild(self, child):
		self.__children.append(child)

	def print(self):
		s = self.__indent + "Attribute: "
		if not self.__suffix is "" :
			s += self.__suffix + " : "
		p = 0
		n = 0
		if len(self.__sorted_examples) == 2 :
			p = len(self.__sorted_examples[0])
			n = len(self.__sorted_examples[1])
		print(s, self.__attribute, " : [", p, ", ", n, "]")
		#print(s, self.__attribute, " : ", self.__sorted_examples)
		for child in self.__children :
			child.print()
		#print("Options: ", self.__options, ", with corresponding children: ", self.__children)
