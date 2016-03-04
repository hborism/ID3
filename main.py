import reader
import tree
import sys

f = open('output.dot', 'w')
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
	dot = t.exportDot()
	f.write(dot)
