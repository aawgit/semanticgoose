import re
from vector_db.vector_db import VectorDB
import chromadb


class Chroma(VectorDB):
    def __init__(self):
        super().__init__()
        self.client = chromadb.PersistentClient(path="./vector_db/storage")

    def insert(self, embedding, phrase):
        pass

    def get(self, document_name, phrase):
        check_collection_name(document_name)
        collection = self.client.get_collection(name=document_name)
        results = collection.query(
            query_texts=[phrase],
            n_results=3
        )
        return results['documents']

    def bulk_insert(self, document_name, phrases, embeddings=None):
        check_collection_name(document_name)
        try:
            collection = self.client.get_collection(name=document_name)
            # TODO: Better way
            return document_name
        except Exception as e:
            pass
        collection = self.client.create_collection(name=document_name)
        collection.add(
            documents=phrases,
            ids=[str(i) for i in range(0, len(phrases))]
        )
        return document_name

def check_collection_name(name):
    # Check if the length is between 3 and 63 characters.
    if not 3 <= len(name) <= 63:
        return "Invalid: The length of the name must be between 3 and 63 characters."

    # Check if the name starts and ends with a lowercase letter or a digit.
    if not re.match(r'^[a-z0-9].*[a-z0-9]$', name):
        return "Invalid: The name must start and end with a lowercase letter or a digit."

    # Check for consecutive dots.
    if '..' in name:
        return "Invalid: The name must not contain two consecutive dots."

    # Check if the name is a valid IP address.
    def is_valid_ip(ip):
        parts = ip.split('.')
        if len(parts) != 4:
            return False
        try:
            return all(0 <= int(part) <= 255 for part in parts)
        except ValueError:
            return False

    if is_valid_ip(name):
        return "Invalid: The name must not be a valid IP address."

    # If all checks pass, return the name as is.
    return name
