class DocumentData:
    sparse_list = []
    topic = ""

    def __init__(self, sparse_list, topic):
        self.sparse_list = sparse_list
        self.topic = topic
        self.vector_rep = []
