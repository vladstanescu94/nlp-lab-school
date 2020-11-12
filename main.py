import numpy as np
import random

from config_constants import PATH_MINI
from file_manager import parse_xml_files, write_data_to_arrf_file
from nlp import generate_topics_dictionary, get_file_words
from helpers import generate_global_words_list, generate_word_count_dictionary
from sklearn import metrics

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

    print("Number of files " + str(len(dictionaries_list)))
    print("Words in global dictionary " + str(len(global_list)))

    distinct_topics = set()

    for topic_entry in topics_list:
        topics = topic_entry['FILE_TOPICS']
        for topic in topics:
            distinct_topics.add(topic)

    vector_space_matrix = []

    for dictionary in dictionaries_list:
        file_vector = []
        for word in global_list:
            if word not in dictionary:
                file_vector.append(0)
                continue
            file_vector.append(dictionary[word])

        vector_space_matrix.append(file_vector)

    write_data_to_arrf_file("data.arrf", global_list,
                            distinct_topics, vector_space_matrix, topics_list)

    # matrix = np.array(vector_space_matrix)
    # print(matrix.shape)
