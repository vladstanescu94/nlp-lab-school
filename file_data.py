class FileData:
    words_freq = {}
    vector_representation = []

    def __init__(self, file_id, words, topics):
        self.file_id = file_id
        self.words = words
        self.topics = topics

    def generate_file_data(self, global_corpus):
        self._generate_word_count_dictionary()
        self.generate_vector_representation(global_corpus)

    def _generate_word_count_dictionary(self):
        self.words_freq = {}
        for word in self.words:
            if word not in self.words_freq:
                self.words_freq[word] = 1
            else:
                self.words_freq[word] += 1

    def generate_vector_representation(self, global_corpus):
        self.vector_representation = []
        for word in global_corpus:
            if word not in self.words_freq:
                self.vector_representation.append(0)
            else:
                self.vector_representation.append(self.words_freq[word])
