from dotenv import load_dotenv

load_dotenv()

from . import make_docs


class StuffChain:

  def __init__(self, model_kwargs):
    self.llm = self.make_llm(**model_kwargs)
    self.chain = self.make_chain(self.llm)

  def make_llm(self, model_name="text-davinci-003", temperature=0.):
    from langchain.llms import OpenAI

    llm = OpenAI(temperature=temperature, model_name=model_name)

    return llm

  def make_chain(self, llm):
    from langchain.chains.qa_with_sources import load_qa_with_sources_chain

    chain = load_qa_with_sources_chain(llm, chain_type="stuff")

    return chain

  def __call__(self, *args, **kwargs):
    return self.chain(*args, **kwargs)


class Runner:

  def __init__(self, chain, docstore):
    self.chain = chain
    self.docstore = docstore

  def __call__(self, query):
    raise NotImplementedError


class StuffChainRunner(Runner):

  def __call__(self, query):
    proposed_docs =  self.docstore[query]
    output = self.chain({"input_documents": proposed_docs, "question": query}, return_only_outputs=True)

    return output["output_text"]


class DocumentStore:

  def __getitem__(self, query):
    raise NotImplementedError


class FaissDocumentStore(DocumentStore):

  def __init__(self, documents, metadatas):
    self.documents = documents
    self.metadatas = metadatas

    self.setup()

  def setup(self):
    from langchain.embeddings.openai import OpenAIEmbeddings

    self.embeddings = OpenAIEmbeddings()  # uses ada-002 by default

    from langchain.vectorstores.faiss import FAISS
    # https://github.com/facebookresearch/faiss

    docsearch = FAISS.from_texts(self.documents, self.embeddings, metadatas=self.metadatas)

    self._store = docsearch

  def __getitem__(self, query):
    return self._store.similarity_search(query)


def get_runner():
  texts, metadatas = make_docs.produce_documents()
  docsearch = FaissDocumentStore(texts, metadatas)

  chain = StuffChain({"model_name": "text-davinci-003", "temperature": 0.0})

  query_runner = StuffChainRunner(chain, docsearch)

  return query_runner
