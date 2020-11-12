import contractions

from nltk import word_tokenize, pos_tag
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer, PorterStemmer
from helpers import lowercase_words, remove_symbols_and_numbers

ps = PorterStemmer()
lemmatizer = WordNetLemmatizer()
stop_words = stopwords.words('english')
stop_words.append('reuters')
stop_words.append('Reuters')


def get_file_words(root, stemming=False):
    file_words = []
    title_content = get_element_content_from_file(root, 'title')
    text_content = get_element_content_from_file(root, 'p')
    file_content = title_content + text_content
    file_words += generate_word_list(file_content, stemming)
    return file_words


def get_element_content_from_file(root, element_name):
    content = ""
    for element in root.iter(element_name):
        content += element.text
    return content


def generate_word_list(text, stemming):
    text_no_contractions = remove_contractions(text)
    tokens = tokenize(text_no_contractions)
    words_lower = lowercase_words(tokens)
    words_no_symbols = remove_symbols_and_numbers(words_lower)
    words_no_stopwords = remove_stop_words(words_no_symbols)
    if stemming:
        words_clean = stem_words(words_no_stopwords)
    else:
        words_clean = lemmatize_words(words_no_stopwords)
    return words_clean


def remove_contractions(text):
    return contractions.fix(text)


def tokenize(text):
    return word_tokenize(text)


def remove_stop_words(words):
    return [word for word in words if not word in stop_words]


def lemmatize_words(words):
    lematized_words = []
    tags = pos_tag(words)

    for word, tag in tags:
        lematized_words.append(lemmatizer.lemmatize(
            word, pos=get_wordnet_pos(tag)))

    return lematized_words


def stem_words(words):
    return [ps.stem(word) for word in words]


def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    if treebank_tag.startswith('V'):
        return wordnet.VERB
    if treebank_tag.startswith('N'):
        return wordnet.NOUN
    if treebank_tag.startswith('R'):
        return wordnet.ADV
    return wordnet.NOUN


def generate_topics_dictionary(root):
    file_data = {}
    file_data['FILE_ID'] = root.attrib['itemid']
    file_topics = []
    for codes in root.iter('codes'):
        if codes.attrib['class'] == "bip:topics:1.0":
            for child in codes:
                file_topics.append(child.attrib['code'])
    file_data['FILE_TOPICS'] = file_topics
    return file_data
