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
