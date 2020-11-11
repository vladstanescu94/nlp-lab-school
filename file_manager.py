import os
import xml.etree.ElementTree as ET


def parse_xml_files(path):
    trees = []
    try:
        for filename in os.listdir(path):
            if not filename.endswith('.XML'):
                continue
            fullname = os.path.join(path, filename)
            tree = ET.parse(fullname)
            trees.append(tree)
    except FileNotFoundError as file_not_found:
        print("Error : " + file_not_found)
    return trees


def write_data_to_arrf_file(filename, global_list, distinct_topics, vector_space_matrix, topics_list):
    file_writter = open(filename, "w")

    for word in global_list:
        file_writter.write(f'@attribute {word} NUMERIC\n')

    file_writter.write("\n")

    for topic in distinct_topics:
        file_writter.write(f'@topics {topic}\n')

    file_writter.write("\n")
    file_writter.write("@data")
    file_writter.write("\n")

    for index, entry in enumerate(vector_space_matrix):
        for instance in entry:
            file_writter.write(f'{instance[0]}:{instance[1]},')
        file_writter.write(' # ')
        topics = topics_list[index]['FILE_TOPICS']
        for topic in topics:
            file_writter.write(f'{topic}, ')
        file_writter.write("\n")

    file_writter.close()
