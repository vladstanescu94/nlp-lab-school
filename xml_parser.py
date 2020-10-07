import xml.etree.ElementTree as ET
import os

from helpers import generateWordList

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

def getTitleTagContent(root):
    title_tag = root.find('title')
    title_content = generateWordList(title_tag.text)
    return title_content

def getTextTagContent(root):
    text_content = []
    for text_tag in root.findall('text'):
        for p_tag in text_tag.findall('p'):
            text_content += generateWordList(p_tag.text)
    return text_content