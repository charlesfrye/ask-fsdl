from dotenv import load_dotenv

load_dotenv()

import os

from . import make_docs
from .chainrunner import *
from .docstore import *


def get_runner(regenerate=False):
  from pathlib import Path
  filename = Path(FaissDocumentStore.filename).resolve()

  if regenerate or not os.path.exists(filename):
      texts, metadatas = make_docs.produce_documents()
      docsearch = FaissDocumentStore.from_texts(texts, metadatas)
      docsearch.to_pickle()
  else:
      docsearch = FaissDocumentStore.from_pickle()

  chain = StuffChain({"model_name": "text-davinci-003", "temperature": 0.0})

  query_runner = StuffChainRunner(chain, docsearch)

  return query_runner
