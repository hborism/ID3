import os
import sys
import math
import copy

class Tree:
	
	def __init__(self, data, attributes, options):
		self.data = data
		self.attributes = attributes
		self.options = options
		self.nbr_o_ex = len(data)
		self.goal_entropy=-1
		self.root=0

		#find the goal_entorpy
		#x is the position of the goal attribute in self.data
		self.goal_pos = len(attributes) - 1
		self.goal = attributes[-1:][0]
		self.goal_opts = options[self.goal_pos]
		#p is the number of positive outcomes of the goal function in our examples
		outcomes = options[self.goal_pos]
		p_outcomes = [0 for i in range(len(outcomes))]
		for d in data :
			g_val = d[self.goal_pos]
			p_outcomes[g_val] += 1
		# entropy of goal
		self.goal_entropy=self.entropy(p_outcomes)
		print("Goal entropy: ", self.goal_entropy)

	def entropy(self, p_outcomes) :
		entropy = 0
		for k in p_outcomes :
			if k == 0 :
				continue
			P_vk = k / sum(p_outcomes)
			entropy += (P_vk * math.log(P_vk, 2))
		return -entropy

	def getRoot(self):
		return self.root

	def getAttributes(self):
		return self.attributes

	def goalEntropy(self):
		return self.goal_entropy

	def gain(self, attribute, sorted_examples):
		if attribute not in self.attributes:
			return -1

		#find position of attribute
		index = self.attributes.index(attribute)

		#calculate the number of examples
		ex_count = 0
		for examples in sorted_examples :
			ex_count += len(examples)
		
		if ex_count == 0:
			return 0

		#creating a tree for this attribute (look at fig 18.4 in book)
		opt_count = len(self.options[index])
		result = [[0 for i in range(len(self.goal_opts))] for j in range(opt_count)]

		for outcomes in sorted_examples:
			for o in outcomes:
				result[o[index]][o[self.goal_pos]]+=1
		
		#calculate the remainder
		
		remainder=0
		for c in range(opt_count):
			if sum(result[c]) == 0 :
				continue
			remainder += (sum(result[c])/ex_count)*(self.entropy(result[c]))


		#return goal entropy minus the remainder (see page 704 in book)
		return self.goal_entropy-remainder


	def sortExamples(self, examples):
		sorted_examples = [[] for i in range(len(self.goal_opts))]
		for ex in examples:
			sorted_examples[ex[self.goal_pos]].append(ex)
		
		return sorted_examples

	def importance(self, attributes, examples):
		maxgain = -1
		maxgain_attribute = ""
		for x in attributes:
			gain = self.gain(x, examples)
			if gain > maxgain:
				maxgain = gain
				maxgain_attribute = x
		return maxgain_attribute

	def buildTree(self):
		attributes=copy.copy(self.attributes)
		#print(self.goal)
		#print(attributes)
		attributes.remove(self.goal)

		attribute=self.importance(attributes,self.sortExamples(self.data))
		options=self.options[self.attributes.index(attribute)]

		#create root node
		self.root=Node(attribute,self.sortExamples(self.data),options, "", "")

		self.populateTree(self.root)


	def populateTree(self, parentNode):
		options=parentNode.getOptions()
		sorted_examples=parentNode.getSortedExamples()
		attribute_pos=self.attributes.index(parentNode.getAttribute())
		sorted_examples_per_option=[]
		indent = parentNode.getIndent() + "\t"

		for op in range(len(options)):
			temp_examples=[]
			for outcome in sorted_examples:
				for example in outcome:
					if example[attribute_pos]==op:
						temp_examples.append(example)
			temp_examples=self.sortExamples(temp_examples)
			sorted_examples_per_option.append(temp_examples)
		#check that it works by printing. it produces the examples sorted as in figure 18.4
		#print(sorted_examples_per_option)
		lengths = list(map(len, sorted_examples)) 
		#lengths = list(map(len, sorted_examples_per_option))
		l_sum = sum(lengths)
		#print(l_sum, " : ", lengths)
		#walk through each option to see if a child shall be a leaf or node
		for op in range(len(options)):
			option = options[op]
			temp_lengths = list(map(len, sorted_examples_per_option[op]))
			temp_sum = sum(temp_lengths)
			focusNode=0
			found = False
			for i in range(len(temp_lengths)) :
				if temp_sum - temp_lengths[i] == 0 :
					goal = self.goal_opts[i]
					focusNode = Node(option, sorted_examples_per_option[op], [], indent, "")
					parentNode.addChild(focusNode)
					found = True
					break
			if not found :
				attributes=copy.copy(self.attributes)
				attributes.remove(parentNode.getAttribute())
				attributes.remove(self.goal)
				child_attribute=self.importance(attributes,sorted_examples_per_option[op])
				#print(child_attribute)
				child_attribute_pos=self.attributes.index(child_attribute)
				child_options=self.options[child_attribute_pos]
				focusNode=Node(child_attribute,sorted_examples_per_option[op],child_options, indent, option)
				#print(focusNode.getAttribute())
				parentNode.addChild(focusNode)

				#recursion
				self.populateTree(focusNode)
#			print(focusNode.getSuffix(), focusNode.getAttribute(),  focusNode.getSortedExamples())

	def exportDot(self) :
		head = "digraph g {"
		nodes = self.root.dotNode(0)
		body = self.root.dot()
		tail = "}"
		dot_string = head + "\n"
		for s in (nodes + body) :
			dot_string += "\t" + s + "\n"
		dot_string += tail + "\n"
		return dot_string

class Node:
	def __init__(self, attribute, examples, options, indent, suffix):
		self.attribute=attribute
		self.sorted_examples=examples
		self.options=options
		self.children=[]
		self.indent = indent
		self.suffix = suffix
		self.ID = ""

	def getIndent(self):
		return self.indent

	def getAttribute(self):
		return self.attribute

	def getSortedExamples(self):
		return self.sorted_examples

	def getOptions(self):
		return self.options

	def getChildren(self):
		return self.children

	def addChild(self, child):
		self.children.append(child)
	
	def getSuffix(self):
		return self.suffix
	
	def getID(self):
		return self.ID

	def dotNode(self, index) :
		lengths = list(map(len, self.sorted_examples))
		self.ID = "struct" + str(index)
		node_info = []
		node = self.ID
		node += "[shape=record, label=\"{ "
		node += self.attribute
		node += " |{"
		for l in lengths :
			node += str(l) + " | "
		node = node[:-3]
		node += "}}\"]"
		node_info.append(node)
		index *= 10
		for child in self.children :
			index += 1
			node_info[len(node_info):] = child.dotNode(index)
		return node_info

	def dot(self):
		edges = []
		for i in range(len(self.children)) :
			s = "\"" + self.ID + "\""
			s += " -> \"" + self.children[i].getID() + "\""
			s += " [label=\""
			s += self.options[i] + "\"];"
			edges.append(s)
		for child in self.children :
			edges[len(edges):] = child.dot()
		return edges
		

	def print(self):
		s = self.indent
		if not self.suffix is "" :
			s += self.suffix + " : "
		s += self.attribute + " : ["
		for ex in self.sorted_examples :
			s += str(len(ex)) + ", "
		s = s.strip(", ") + "]"
		print(s)
		for child in self.children :
			child.print()
