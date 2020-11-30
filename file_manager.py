def write_data_to_arrf_file(filename, global_list, file_data_list):
    distinct_topics = set()

    for file_data in file_data_list:
        for topic in file_data.topics:
            distinct_topics.add(topic)

    file_writter = open(filename, "w")

    for word in global_list:
        file_writter.write(f'@attribute {word} NUMERIC\n')

    file_writter.write("\n")
    file_writter.write(f'@attribute class {distinct_topics}\n')
    file_writter.write("\n")

    for topic in distinct_topics:
        file_writter.write(f'@topics {topic}\n')

    file_writter.write("\n")
    file_writter.write("@data")
    file_writter.write("\n")

    for file_data in file_data_list:
        for i, entry in enumerate(file_data.vector_representation):
            if entry == 0:
                continue
            file_writter.write(f'{i}:{entry},')
        file_writter.write(' # ')
        for topic in file_data.topics:
            file_writter.write(f"{topic},")
        file_writter.write("\n")
    file_writter.close()
