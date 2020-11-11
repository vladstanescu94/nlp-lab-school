import pprint

from config_constants import *
from xml_parser import parse_xml_files
from nlp import generate_topics_dictionary, get_file_words
from helpers import generate_global_words_list, generate_word_count_dictionary

global_list = []

if __name__ == "__main__":
    dictionaries_list = []
    topics_list = []

    files = parse_xml_files(PATH_MINI)

    for file in files:
        root = file.getroot()
        file_words = get_file_words(root)

        file_dict = generate_word_count_dictionary(file_words)
        file_dict['FILE_ID'] = root.attrib['itemid']
        dictionaries_list.append(file_dict)
        file_topics = generate_topics_dictionary(root)
        topics_list.append(file_topics)

        generate_global_words_list(global_list, file_words)

    for dictionary in dictionaries_list:
        pprint.pprint(dictionary)
        print('----------------------------')

    print("Number of files " + str(len(dictionaries_list)))
    print("Words in global dictionary " + str(len(global_list)))
    print('----------------------------')
    for topic in topics_list:
        print(topic)
    # distinct_topics = []

    # for topic_entry in topics_list:
    #     topics = topic_entry['FILE_TOPICS']
    #     for topic in topics:
    #         if topic in distinct_topics:
    #             continue
    #         distinct_topics.append(topic)
    # print(distinct_topics)

    # for topic_entry in topics_list:
    #     topics = topic_entry['FILE_TOPICS']

    # vector_space_matrix = []
    # for dictionary in dictionaries_list:
    #     vector = []
    #     for item in global_list:
    #         if item in dictionary:
    #             vector.append((global_list.index(item), dictionary[item]))
    #     vector_space_matrix.append(vector)

    # print(vector_space_matrix[0])
