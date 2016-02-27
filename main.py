import os
import sys


class ARFFreader:

    __filename = ""
    __relation = ""
    __attributes=[]
    __options=[]
    __data=[]

    def __init__(self, filename):


        self.__filename=filename
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


        print(self.relation())
        print(self.attributes())
        print(self.options())
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



print("Welcome to ID3!")
#print("Try to follow the instructions as closely as possible,\nthis program does not handle errors.")
#filename = input("Input the file name\n")
r=ARFFreader("waitfortable.arff")
print(r.relation())
print(r.attributes())
print(r.options())
print(r.data())
