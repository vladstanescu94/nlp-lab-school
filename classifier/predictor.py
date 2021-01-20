import os
import numpy as np
from arff_parser import parse_arff

from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report


def main():

    arff_path = os.path.abspath("../data-selected-full.arff")
    corpus, topics, file_data_list = parse_arff(arff_path)
    generate_vector_rep(corpus, file_data_list)

    matrix = generate_vector_matrix(file_data_list)
    target = generate_target_vector(file_data_list, topics)

    X_train, X_test, y_train, y_test = train_test_split(
        matrix, target, test_size=0.3,)

    model = MultinomialNB()
    model.fit(X_train, y_train)
    predict = model.predict(X_test)
    print(f"Prediction accuracy: {accuracy_score(y_test, predict)}")

    print(classification_report(y_test, predict, target_names=topics))


def generate_vector_rep(corpus, file_data_list):
    for file in file_data_list:
        for _ in corpus:
            file.vector_rep.append(0)

        for entry in file.sparse_list:
            file.vector_rep[int(entry[0])] = int(entry[1])


def generate_vector_matrix(file_data_list):
    vector_matrix = []
    for file in file_data_list:
        vector_matrix.append(file.vector_rep)

    return np.asarray(vector_matrix)


def generate_target_vector(file_data_list, topics):
    target_vector = []

    for file in file_data_list:
        topic_index = topics.index(file.topic)
        target_vector.append(topic_index)

    return target_vector


if __name__ == "__main__":
    print("Starting document classifier\n")
    main()
    print("Job Done\n")
