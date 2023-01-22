from langchain.embeddings.openai import OpenAIEmbeddings

from cache_to_disk import cache_to_disk

from langchain.vectorstores.faiss import FAISS
# https://github.com/facebookresearch/faiss


class DocumentStore:

  def __getitem__(self, query):
    raise NotImplementedError


class FaissDocumentStore(DocumentStore):

  def __init__(self, documents, metadatas):
    self.documents = documents
    self.metadatas = metadatas

    self.setup()

  @cache_to_disk(30)
  def setup(self):

    self.embeddings = OpenAIEmbeddings()  # uses ada-002 by default

    docsearch = FAISS.from_texts(self.documents, self.embeddings, metadatas=self.metadatas)

    self._store = docsearch

  def __getitem__(self, query):
    return self._store.similarity_search(query)
