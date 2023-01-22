from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.faiss import FAISS


class DocumentStore:

  def __getitem__(self, query):
    raise NotImplementedError


class FaissDocumentStore(DocumentStore):
  filename = "documents/stored.pkl"

  def __init__(self, store):
    self.store = store

  @classmethod
  def from_texts(cls, texts, metadatas):
    embeddings = OpenAIEmbeddings()  # uses ada-002 by default
    docsearch = FAISS.from_texts(texts, embeddings, metadatas=metadatas)

    return cls(docsearch)

  @classmethod
  def from_pickle(cls, filename=None):
    import pickle

    if filename is None:
      filename = cls.filename

    with open(filename, "rb") as f:
      store = pickle.load(f)

    return cls(store)

  def to_pickle(self, filename=None):
    import pickle

    if filename is None:
      filename = self.filename

    with open(filename, "wb") as f:
      pickle.dump(self.store, f)

  def __getitem__(self, query):
    return self.store.similarity_search(query)
