from dotenv import load_dotenv

load_dotenv()

from . import make_docs
from .chainrunner import *
from .docstore import *


def get_runner():
  texts, metadatas = make_docs.produce_documents()
  docsearch = FaissDocumentStore(texts, metadatas)

  chain = StuffChain({"model_name": "text-davinci-003", "temperature": 0.0})

  query_runner = StuffChainRunner(chain, docsearch)

  return query_runner
