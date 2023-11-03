from document import Document
from constants import Constants
from language_model.language_model import LanguageModel
from vector_db.vector_db import VectorDB

# Get the chunks
file = "sample.txt"
document = Document(file)
document.clean()
chunks = document.get_chunks(Constants.CHUNK_BY_PARAGRAPH)

# Get vectors
lm = LanguageModel()
embeddings = [lm.get_vector(chunk) for chunk in chunks]

# Insert to the vectorDB
db = VectorDB()
db.bulk_insert(chunks, embeddings, document.name)