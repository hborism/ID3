import reader
import tree
import sys

argv = sys.argv[1:]
for file_name in argv :
	print("Filename : ", file_name)
	r=reader.ARFFreader(file_name)
	#print(r.relation())
	#print(r.attributes())
	#print(r.options())
	#print(r.data())
	t=tree.Tree(r.data(),r.attributes(),r.options())
	#print(t.goalEntropy())
	t.buildTree()
	abc=t.getRoot()
	abc.print()
#	t=tree.Tree(r.data(),r.attributes(),r.options(),"goal")
#	t.buildTree()
#	abc=t.getRoot()
#	abc.print()
	
	
"""

t=tree.Tree(r.data(),r.attributes(),r.options(),"goal")
print(t.goalEntropy())

t.buildTree()
abc=t.getRoot()

abc.print()

def print_node(node) :
	node.print()
	children = node.getChildren()
	if len(children) == 0 :
		return
	for child in children :
		print_node(child)

print_node(abc) """
