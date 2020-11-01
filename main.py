import os
import pprint

from xml_parser import parse_xml_files
from nlp import generate_topics_dictionary, get_file_words
from helpers import generate_global_words_list, generate_word_count_dictionary

path_mini = os.path.abspath("./Resources/Reuters_34/Training/")
path_full = os.path.abspath("./Resources/Reuters_7083/Training/")

globalList = []

if __name__ == "__main__":
    dictionaries_list = []
    topics_list = []

    files = parse_xml_files(path_mini)

    for file in files:
        root = file.getroot()
        file_words = get_file_words(root)

        file_dict = generate_word_count_dictionary(file_words)
        file_dict['FILE_ID'] = root.attrib['itemid']
        dictionaries_list.append(file_dict)
        file_topics = generate_topics_dictionary(root)
        topics_list.append(file_topics)

        generate_global_words_list(globalList, file_words)

    globalList.sort()

    for dictionary in dictionaries_list:
        pprint.pprint(dictionary)
        print('----------------------------')

    print("Number of files " + str(len(dictionaries_list)))
    print("Words in global dictionary " + str(len(globalList)))
    print('----------------------------')
    for topic in topics_list:
        print(topic)
