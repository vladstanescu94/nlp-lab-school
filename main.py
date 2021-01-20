import os
import bisect
import math
import numpy as np

from config_constants import PATH_MINI, PATH_FULL
from dataset_representation import DatasetRepresentation
from file_data import FileData
from xml_manager import parse_xml_files
from file_manager import write_data_to_arff_file
from nlp import get_file_words, get_file_topics


def main():
    files = parse_xml_files(os.path.abspath(PATH_FULL))
    no_examples = len(files)
    global_list = []
    file_data_list = []

    for file in files:
        root = file.getroot()

        file_id = root.attrib['itemid']
        file_words = get_file_words(root, stemming=False)

        for word in file_words:
            if word in global_list:
                continue
            bisect.insort(global_list, word)

        topics = get_file_topics(root)
        file_data = FileData(file_id, file_words, topics)
        file_data_list.append(file_data)

    for file_data in file_data_list:
        file_data.generate_file_data(global_list)

    data_rep = DatasetRepresentation(file_data_list, global_list)
    data_rep.clean_topics()

    print(f"Number of files {no_examples} ")
    print(f"Words in global dictionary {len(global_list)}")

    data_rep.generate_vector_matrix()

    information_gain_list = information_gain(data_rep, global_list)
    sorted_list = sorted(information_gain_list, key=lambda x: x[0])
    new_global = []
    for entry in sorted_list:
        index = entry[0]
        new_global.append(global_list[index])

    for data in data_rep.file_data_list:
        data.generate_vector_representation(new_global)

    write_data_to_arff_file("data-selected-full.arff", new_global,
                            data_rep)


def entropy(data_rep):
    entropy_sum = 0
    for topic in data_rep.distinct_topics:
        documents_with_given_topic = 0
        for doc_data in data_rep.file_data_list:

            if topic in doc_data.topics:
                documents_with_given_topic += 1
        prob = documents_with_given_topic / len(data_rep.file_data_list)

        entropy_sum += prob * math.log2(prob)

    return -entropy_sum


def information_gain(data_rep, global_list):
    set_entropy = entropy(data_rep)
    gains_list = []
    np_matrix = np.asarray(data_rep.vector_matrix)

    for index in range(len(global_list)):
        col = np_matrix[:, index]
        distincte = set(col)
        gain_sum = 0
        for atrib in distincte:
            new_list = []

            for file in data_rep.file_data_list:
                if file.vector_representation[index] == atrib:
                    new_list.append(file)
            new_rep = DatasetRepresentation(new_list, global_list)
            new_rep.test_topics()
            gain_sum += (len(new_list) / len(data_rep.file_data_list)) * \
                entropy(new_rep)
        information_g = set_entropy - gain_sum
        gains_list.append((index, information_g))

    sorted_list = sorted(gains_list, key=lambda x: x[1], reverse=True)
    threshold = len(sorted_list) // 10
    return sorted_list[:threshold]


def generate_vector_matrix(file_data_list):
    print("Generating vector matrix")
    vector_matrix = []

    for file_data in file_data_list:
        if not file_data.topics:
            continue

        for _ in file_data.topics:
            vector_matrix.append(file_data.vector_representation)

    return np.asarray(vector_matrix)


if __name__ == "__main__":
    print("Starting arff generator\n")
    main()
    print("Job Done\n")
