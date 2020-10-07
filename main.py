import os
import pprint

from helpers import generateWordCountDictionary
from xml_parser import parseXMLFiles, getTextTagContent, getTitleTagContent

path_mini = os.path.abspath("./Resources/Reuters_34/Training/")
path_full = os.path.abspath("./Resources/Reuters_7083/Training/")

if __name__ == "__main__":
    files = parseXMLFiles(path_mini)
    dictionaries_list = []

    for file in files:
        root = file.getroot()
        file_words = []
        file_words += getTitleTagContent(file)
        file_words += getTextTagContent(file)
        file_dict = generateWordCountDictionary(file_words)
        dictionaries_list.append(file_dict)
        
    # for d in range(len(dictionaries_list)):
    #     pprint.pprint(dictionaries_list[d])
    pprint.pprint(dictionaries_list[0])