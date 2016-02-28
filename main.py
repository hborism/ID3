import os
import sys
import math
import copy



class ARFFreader:

    __filename = ""
    __relation = ""
    __attributes=[]
    __options=[]
    __data=[]


    def __init__(self, filename):


        #self.__filename=filename
        f = open(filename, 'r')
        text_in_file=f.read()

        #make sure the file containes relation, attribute and data
        if text_in_file.find("@relation")==-1 or text_in_file.find("@attribute")==-1 or text_in_file.find("@data")==-1:
            print("Error: file format")
            print("file should be of structure")
            print("@relation")
            print("@attribute")
            print("@data")


        #read in relataion
        i=text_in_file.index("@relation")
        i=i+10
        while text_in_file[i] != " " and text_in_file[i] !="\n":
            self.__relation=self.__relation+text_in_file[i]
            i+=1

        #read in attributes
        #read in options
        all_attributes=[]
        all_options=[]

        for x in range(0, text_in_file.count("@attribute")):
            i=text_in_file.find("@attribute", i)+10
            i=self.jumpOver(text_in_file,i,[" ", "\t"])
            attribute=""
            while text_in_file[i]!=" " and text_in_file[i]!="{" and text_in_file[i]!="\t":
                attribute=attribute+text_in_file[i]
                i+=1
            all_attributes.append(attribute)

            i=text_in_file.find("{", i)+1
            options=[]
            while text_in_file[i]!="}":
                i=self.jumpOver(text_in_file,i,[" ", ",", "\t"])
                option=""

                while text_in_file[i]!="," and text_in_file[i]!="}"and text_in_file[i]!=" ":
                    option=option+text_in_file[i]
                    i+=1
                options.append(option)

            all_options.append(options)

        self.__attributes=all_attributes
        self.__options=all_options


        #print(self.relation())
        #print(self.attributes())
        #print(self.options())

        #read in data
        i=text_in_file.find("@data", i)+6
        i=self.jumpComments(text_in_file,i)

        all_data=[]
        flag_end_of_doc=0
        line=0
        while flag_end_of_doc==0:
            line+=1
            data_row=[]
            for x in range(0,len(all_attributes)):
                if x!=len(all_attributes)-1:
                    j=text_in_file.find(",", i)
                else:
                    j=text_in_file.find("\n", i)
                    if j==-1:
                        j=len(text_in_file)
                        flag_end_of_doc=1
                datacell=text_in_file[i:j]
                for y in range(0, len(all_options[x])):
                    if datacell==all_options[x][y]:
                        data_row.append(y)
                        if flag_end_of_doc==0:
                            i=self.jumpOver(text_in_file,j+1,[" ", "\t"])
                        break
                    if y==len(all_options[x])-1:
                        print("Error reading data")
                        print("Data line: ", line)
                        print("Attribute: ", all_attributes[x])
                        print("Please restart program and enter a valid ARFF-file")
                        exit()
            all_data.append(data_row)
            i=self.jumpOver(text_in_file,i,[" ", "\n", "\t"])

        self.__data=all_data

    def relation(self):
        return self.__relation

    def attributes(self):
        return self.__attributes

    def options(self):
        return self.__options

    def data(self):
        return self.__data

    # jump over specific characters in text
    def jumpOver(self,text_in_file, i,list):
        while text_in_file[i] in list:
            i+=1
        return i

    def jumpComments(self,text_in_file,i):
        i=self.jumpOver(text_in_file,i,["\n", "\t", " "])
        while text_in_file[i]=="%":
            while text_in_file[i]!="\n":
                i+=1
            i+=1
        i=self.jumpOver(text_in_file,i,["\n", "\t", " "])
        return i


#---------------------------------data manipulation----------------------------------


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
        goal_pos=0
        while attributes[goal_pos]!=goal:
            goal_pos+=1
        self.__goal_pos=goal_pos

        #p is the number of positive outcomes of the goal function in our examples
        p=0
        self.__no_examples=len(data)
        for i in range(0,self.__no_examples):
            p=p+data[i][goal_pos]

        # entropy of goal
        self.__goal_entropy=self.entropy((p/self.__no_examples))

    def entropy(self,q):
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
        self.__root=Node(attribute,self.sortExamples(self.__data),options)

        self.__root.print()

        focusNode=Node("Hello",[1,3,2,3,],[])
        focusNode2=Node("Goodbye",[1,3,2,3,],[])

        focusNode.addChild(focusNode2)


        self.populateTree(self.__root)


    def populateTree(self, parentNode):
        options=parentNode.getOptions()
        sorted_examples=parentNode.getSortedExamples()
        attribute_pos=self.__attributes.index(parentNode.getAttribute())
        sorted_examples_per_option=[]

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
        for op in range(0,len(options)):
            abc=(sorted_examples_per_option[op])
            if len(sorted_examples_per_option[op][0])==0 and len(sorted_examples_per_option[op][1])==0:
                focusNode=Node("Yes/no",[],[])
                parentNode.addChild(focusNode)
            elif len(sorted_examples_per_option[op][0])==0:
                focusNode=Node("No",sorted_examples_per_option[op],[])
                parentNode.addChild(copy.copy(focusNode))
            elif len(sorted_examples_per_option[op][1])==0:
                focusNode=Node("Yes",sorted_examples_per_option[op],[])
                parentNode.addChild(focusNode)
            else:
                attributes=copy.copy(self.__attributes)
                attributes.remove(parentNode.getAttribute())
                attributes.remove(self.__goal)
                child_attribute=self.importance(attributes,sorted_examples_per_option[op])
                child_attribute_pos=self.__attributes.index(child_attribute)
                child_options=self.__options[child_attribute_pos]
                focusNode=Node(child_attribute,sorted_examples_per_option[op],child_options)
                parentNode.addChild(focusNode)

                #recursion
                self.populateTree(focusNode)


class Node:
    __attribute=""
    __sorted_examples=[]
    __options=[]
    __children=[]

    def __init__(self, attribute, examples, options):
        self.__attribute=attribute
        self.__sorted_examples=examples
        self.__options=options

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
        print("Attribute: ", self.__attribute)
        print("Examples (sorted): ", self.__sorted_examples)
        print("Options: ", self.__options, ", with corresponding children: ", self.__children)


print("Welcome to ID3!")
#print("Try to follow the instructions as closely as possible,\nthis program does not handle errors.")
#filename = input("Input the file name\n")
r=ARFFreader("waitfortable.arff")
print(r.relation())
print(r.attributes())
print(r.options())
print((r.data()))

t=Tree(r.data(),r.attributes(),r.options(),"goal")
print(t.goalEntropy())

t.buildTree()

abc=t.getRoot()
abc.print()