import new_reader
import reader
import tree

print("Welcome to ID3!")
#print("Try to follow the instructions as closely as possible,\nthis program does not handle errors.")
#filename = input("Input the file name\n")
r=new_reader.ARFFreader("waitfortable.arff")
#r=reader.ARFFreader("waitfortable.arff")
print(r.relation())
print(r.attributes())
print(r.options())
print(r.data())

t=tree.Tree(r.data(),r.attributes(),r.options(),"goal")
print(t.goalEntropy())

t.buildTree()
abc=t.getRoot()

abc.print()
"""
def print_node(node) :
	node.print()
	children = node.getChildren()
	if len(children) == 0 :
		return
	for child in children :
		print_node(child)

print_node(abc) """
