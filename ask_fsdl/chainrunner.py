from dotenv import load_dotenv

load_dotenv()


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
