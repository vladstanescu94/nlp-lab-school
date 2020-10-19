import os
import pprint

from xml_parser import parseXMLFiles
from nlp import generateCountDictionaiesList

path_mini = os.path.abspath("./Resources/Reuters_34/Training/")
path_full = os.path.abspath("./Resources/Reuters_7083/Training/")

globalList = []

if __name__ == "__main__":
    files = parseXMLFiles(path_mini)
    dictionaries_list = generateCountDictionaiesList(files)
        
    for d in range(len(dictionaries_list)):
        pprint.pprint(dictionaries_list[d])
        print('----------------------------')
        
    print("Number of files " + str(len(dictionaries_list)))
    print("Words in global dictionary " + str(len(globalList)))