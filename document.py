import os
import re
from constants import Constants
from PyPDF2 import PdfReader
import logging
import nltk

class Document:
    def __init__(self, file):
        self.name = os.path.basename(file)
        # TODO: Handle None texts (pdfs that cant be parsed)
        self.text = self.load(file)

    def load(self, file, dump_text=True):
        dump_path = "./text_files/{}.txt".format(self.name)
        if os.path.isfile(dump_path):
            logging.info("Loading from the previous dump.")
            with open(dump_path) as f:
                return f.read()

        if file.split(".")[-1].lower() != "pdf":
            raise Exception("File type is not recognized")
        with open(file, 'rb') as file:
            logging.info("Reading the file {}".format(file))
            pdf = PdfReader(file)
            text = " ".join(page.extract_text() for page in pdf.pages)
        self.text = text
        if dump_text:
            with open(dump_path, "w") as text_file:
                text_file.write(text)
        logging.info("Loaded")

    def clean(self):
        # TODO: Implement pre-processing
        pass

    def get_chunks(self, chunk_by, overlap=3):
        if chunk_by == Constants.CHUNK_BY_SENTENCE:
            return split_text_with_overlap(self.text, num_sentences=5)


def split_text_with_overlap(text, num_sentences=3, overlap=1):
    """
    Splits the input text into multiple chunks, where each chunk contains
    a specified number of sentences with an overlap of a specified number
    of sentences.

    Args:
    - text (str): The input text to be split.
    - num_sentences (int): The number of sentences to include in each chunk.
      Default is 3.
    - overlap (int): The number of sentences to overlap between adjacent
      chunks. Default is 1.

    Returns:
    - A list of text chunks, where each chunk contains a specified number
      of sentences with an overlap of a specified number of sentences.
    """

    # Tokenize the text into sentences using NLTK
    sentences = nltk.sent_tokenize(text)

    # Initialize the list of text chunks
    chunks = []

    # Split the sentences into chunks with the specified overlap
    start_idx = 0
    while start_idx < len(sentences):
        end_idx = min(start_idx + num_sentences, len(sentences))
        chunk = ' '.join(sentences[start_idx:end_idx])
        chunks.append(chunk)
        start_idx += num_sentences - overlap

    return chunks


def clean_file_name(file_path):
    try:
        # Extract the file name from the file path
        file_name = os.path.basename(file_path)

        # Remove non-alphanumeric characters using regular expressions
        cleaned_name = re.sub(r'[^a-zA-Z0-9]', '', file_name)

        # Check if the resulting name is longer than 63 characters
        if len(cleaned_name) > 63:
            raise ValueError("File name is too long")

        return cleaned_name
    except Exception as e:
        return str(e)
