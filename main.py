import os
import bisect
import random
import numpy as np

from sklearn.metrics import normalized_mutual_info_score as score
from sklearn import feature_selection
from config_constants import PATH_MINI, PATH_FULL
from file_data import FileData
from xml_manager import parse_xml_files
from file_manager import write_data_to_arrf_file
from nlp import get_file_words, get_file_topics
from file_data_manager import FileDataManager


def main():
    files = parse_xml_files(os.path.abspath(PATH_MINI))
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

    vector_matrix = []

    for file_data in file_data_list:
        if not file_data.topics:
            continue

        for _ in file_data.topics:
            vector_matrix.append(file_data.vector_representation)

    npmatrix = np.asarray(vector_matrix)
    test_prag = 0.6
    bad_index = []
    for i in range(npmatrix.shape[1]):
        for j in range(1, npmatrix.shape[1]):
            if i != j:
                if i not in bad_index:
                    if j not in bad_index:
                        col_1 = npmatrix[:, i]
                        col_2 = npmatrix[:, j]
                        col_score = score(col_1, col_2)
                        if col_score > test_prag:
                            bad_index.append(i)
                            bad_index.append(j)
                            break

    bad_set = set(bad_index)
    new_global = []
    for i in range(len(global_list)):
        if i in bad_set:
            continue
        new_global.append(global_list[i])

    for file_data in file_data_list:
        file_data.generate_vector_representation(new_global)

    print(len(new_global))
    # print(npmatrix.shape)
    # random_index1 = random.randint(0, len(npmatrix[0]))
    # random_index2 = random.randint(0, len(npmatrix[0]))
    # col_test_1 = npmatrix[:, random_index1]
    # col_test_2 = npmatrix[:, random_index2]
    # print(f"{col_test_1}\n{col_test_2}")
    # print(score(col_test_1, col_test_2))
    write_data_to_arrf_file("data2.arrf", new_global,
                            file_data_manager)


if __name__ == "__main__":
    print("Starting arff generator\n")
    main()
    print("Job Done\n")
