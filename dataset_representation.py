from collections import Counter


class DatasetRepresentation:
    vector_matrix = []

    max_allowance = 0.95
    min_allowance = 0.05

    def __init__(self, file_data_list, global_list):
        self.file_data_list = file_data_list
        self.distinct_topics = []
        self.all_topics = []
        self.global_list = global_list

    def clean_topics(self):
        self._generate_all_topics()
        self._remove_extra_topics()
        self._remove_topics_from_file()
        self._remove_no_topics_file()

    def test_topics(self):
        self._generate_all_topics()
        self.distinct_topics = list(set(self.all_topics))

    def _generate_all_topics(self):
        for file_data in self.file_data_list:
            self.all_topics += file_data.topics

    def _remove_extra_topics(self):
        total_samples = len(self.file_data_list)
        max_bound = self.max_allowance * total_samples
        min_bound = self.min_allowance * total_samples
        topics_freq = Counter(self.all_topics)

        for key in list(topics_freq):
            if topics_freq[key] > max_bound or topics_freq[key] < min_bound:
                topics_freq.pop(key)

        for key in list(topics_freq):
            self.distinct_topics.append(key)

    def _remove_topics_from_file(self):
        set_distinct = set(self.distinct_topics)
        for file_data in self.file_data_list:
            set_topics = set(file_data.topics)
            for topic in set_topics:
                if topic in set_distinct:
                    continue
                file_data.topics.remove(topic)

    def _remove_no_topics_file(self):
        for file_data in self.file_data_list:
            if not file_data.topics:
                self.file_data_list.remove(file_data)

    def generate_vector_matrix(self):
        for file_data in self.file_data_list:
            for _ in file_data.topics:
                self.vector_matrix.append(file_data.vector_representation)
