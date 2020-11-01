def lowercase_words(words):
    return [word.lower() for word in words]


def remove_symbols_and_numbers(words):
    return [word for word in words if word.isalpha()]


def generate_word_count_dictionary(words):
    dictionary = {}
    for word in words:
        if word in dictionary:
            dictionary[word] += 1
        else:
            dictionary[word] = 1
    return dictionary


def generate_global_words_list(global_list, text):
    for word in text:
        if word in global_list:
            continue
        global_list.append(word)
