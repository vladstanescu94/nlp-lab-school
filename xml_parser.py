import os
import xml.etree.ElementTree as ET

def parseXMLFiles(path):
    trees = []
    try:
        for filename in os.listdir(path):
            if not filename.endswith('.XML'): continue
            fullname = os.path.join(path, filename)
            tree = ET.parse(fullname)
            trees.append(tree)
    except Exception as e:
        print("Error : " + e)
    return trees