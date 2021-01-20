from document_data import DocumentData


def parse_arff(arff_file):
    file_reader = open(arff_file, "r")
    corups = []
    topics = []
    file_data_list = []

    for line in file_reader:
        if line.startswith("@attribute"):
            word = line.split(' ')[1]
            corups.append(word)
        elif line.startswith("@topics"):
            topic = line.split(' ')[1].strip("\n")
            topics.append(topic)
        elif line.startswith("@data"):
            continue
        elif line[0].isdigit():
            sparse_list = []
            split_line = line.split(",")
            file_topic = line.split(",")[-1].strip(" # ").strip()

            for i in range(len(split_line) - 1):
                pair = split_line[i].split(":")
                word_index = pair[0]
                word_freq = pair[1]
                sparse_list.append((word_index, word_freq))
            document = DocumentData(sparse_list, file_topic)
            file_data_list.append(document)
    return corups[:-1], topics, file_data_list
