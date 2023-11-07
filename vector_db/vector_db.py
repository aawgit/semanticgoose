class VectorDB:
    def ___init__(self):
        self.client = None

    def insert(self, embedding, phrase):
        pass

    def get(self, document_name, phrase):
        pass

    def bulk_insert(self, document_name, phrases, embeddings=None):
        if embeddings is None:
            embeddings = []
