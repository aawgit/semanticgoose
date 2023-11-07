import logging

logging.basicConfig(level="INFO")

from document import Document, clean_file_name
from constants import Constants
from language_model.language_model import LanguageModel
from vector_db.chroma_db import Chroma


def store(path):
    # Get the chunks
    document = Document(path)
    document.clean()
    chunks = document.get_chunks(Constants.CHUNK_BY_SENTENCE)

    # Get vectors
    lm = LanguageModel()
    embeddings = [lm.get_vector(chunk) for chunk in chunks]

    # Insert to the vectorDB
    doc_name = clean_file_name(path)
    db = Chroma()
    doc_name = db.bulk_insert(doc_name, chunks)
    return doc_name


def search(phrase, document):
    db = Chroma()
    result = db.get(document, phrase)
    for text in result:
        print(text)
        print("\n")
    return result


if __name__ == '__main__':
    # store()
    # search("Why is Hadrian’s-Wall important?", "Hadrian’s-Wall")
    search("Where is Hadrian’s-Wall located?", "Hadrian’s-Wall")
