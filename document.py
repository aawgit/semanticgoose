class Document:
    def __init__(self, file):
        self.name = file
        self.text = None

    def clean(self):
        # TODO: Implement pre-processing
        pass

    def get_chunks(self, chunk_by, overlap=3):
        # TODO
        return [self.text]
