import os
import pprint

from xml_parser import parseXMLFiles
from nlp import  generateTopicsDictionary , getFileWords
from helpers import generateGlobalWordsList, generateWordCountDictionary

path_mini = os.path.abspath("./Resources/Reuters_34/Training/")
path_full = os.path.abspath("./Resources/Reuters_7083/Training/")

globalList = []

if __name__ == "__main__":
    dictionaries_list = []
    topics_list = []

    files = parseXMLFiles(path_mini)

    for file in files:
        root = file.getroot()
        file_words = getFileWords(root)

        file_dict = generateWordCountDictionary(file_words)
        file_dict['FILE_ID'] = root.attrib['itemid']
        dictionaries_list.append(file_dict)
        file_topics = generateTopicsDictionary(root)
        topics_list.append(file_topics)

        generateGlobalWordsList(globalList, file_words)
        
    for d in range(len(dictionaries_list)):
        pprint.pprint(dictionaries_list[d])
        print('----------------------------')
        
    print("Number of files " + str(len(dictionaries_list)))
    print("Words in global dictionary " + str(len(globalList)))
    print('----------------------------')
    for topic in topics_list:
        print(topic)