import os
import bisect
import numpy as np

from sklearn.metrics import normalized_mutual_info_score as score
from config_constants import PATH_MINI, PATH_FULL
from file_data import FileData
from xml_manager import parse_xml_files
from file_manager import write_data_to_arrf_file
from nlp import get_file_words, get_file_topics
from file_data_manager import FileDataManager


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

    file_data_manager = FileDataManager(file_data_list)
    file_data_manager.clean_topics()

    print(f"Number of files {no_examples} ")
    print(f"Words in global dictionary {len(global_list)}")

    vector_matrix = generate_vector_matrix(file_data_list)

    npmatrix = np.asarray(vector_matrix)

    bad_set = generate_bad_attributes_dict(0.58, npmatrix)

    print("Starting feature selection")

    new_global = []
    for i in range(len(global_list)):
        if i in bad_set:
            continue
        new_global.append(global_list[i])

    for file_data in file_data_list:
        file_data.generate_vector_representation(new_global)

    print("Feature selection done")

    print(len(new_global))

    write_data_to_arrf_file("data-full-final.arrf", new_global,
                            file_data_manager)


def generate_vector_matrix(file_data_list):
    print("Generating vector matrix")
    vector_matrix = []

    for file_data in file_data_list:
        if not file_data.topics:
            continue

        for _ in file_data.topics:
            vector_matrix.append(file_data.vector_representation)

    return vector_matrix


def generate_bad_attributes_dict(prag, matrix):
    print("Calculating Mutual info score")
    bad_set = {}
    row_len = matrix.shape[1]
    for i in range(row_len):
        if i in bad_set:
            continue
        col_1 = matrix[:, i]
        for j in range(row_len):
            print(f"iteration i: {i}, j: {j}")
            if j <= i:
                continue
            if j in bad_set:
                continue
            col_2 = matrix[:, j]
            col_score = score(col_1, col_2)
            if col_score > prag:
                bad_set[i] = True
                bad_set[j] = True
    return bad_set


if __name__ == "__main__":
    print("Starting arff generator\n")
    main()
    print("Job Done\n")
