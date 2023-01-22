from .docstore import *
from .chainrunner import *
from . import make_docs
import os
from dotenv import load_dotenv

load_dotenv()


def print_dir():
    current_directory = os.getcwd()
    for file in os.scandir(current_directory):
        if file.is_file():
            print(f'File: {file.name}')
        elif file.is_dir():
            print(f'Directory: {file.name}')
    documents_dir = os.path.join(current_directory, 'documents')
    if (os.listdir(documents_dir)):
        for file in os.scandir(documents_dir):
            if file.is_file():
                print(f'File: {file.name}')
            elif file.is_dir():
                print(f'Directory: {file.name}')


def get_runner(regenerate=False):
    from pathlib import Path
    filename = Path(FaissDocumentStore.filename).resolve()

    print_dir()

    if regenerate or not os.path.exists(filename):
        texts, metadatas = make_docs.produce_documents()
        docsearch = FaissDocumentStore.from_texts(texts, metadatas)
        docsearch.to_pickle()
    else:
        docsearch = FaissDocumentStore.from_pickle()

    print_dir()
    

    chain = StuffChain({"model_name": "text-davinci-003", "temperature": 0.0})

    query_runner = StuffChainRunner(chain, docsearch)

    return query_runner
