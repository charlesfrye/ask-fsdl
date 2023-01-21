from dotenv import load_dotenv

load_dotenv()


def get_runner():
  texts, metadatas = produce_documents()
  docsearch = embed_texts(texts, metadatas)

  llm = make_llm()
  chain = make_chain(llm)

  def query_runner(query):
    return run_query(query, chain, docsearch)

  return query_runner


def make_llm(model_name="text-davinci-003", temperature=0.):
  from langchain.llms import OpenAI

  llm = OpenAI(temperature=temperature, model_name=model_name)

  return llm


def produce_documents():
  import os
  from pathlib import Path
  import string

  lecture_titles = {
    1: "lecture-1-course-vision-and-when-to-use-ml",
    2: "lecture-2-development-infrastructure-and-tooling",
    3: "lecture-3-troubleshooting-and-testing",
    4: "lecture-4-data-management",
    5: "lecture-5-deployment",
    6: "lecture-6-continual-learning",
    7: "lecture-7-foundation-models",
    8: "lecture-8-teams-and-pm",
    9: "lecture-9-ethics"
  }

  lecture_md_url_base = "https://raw.githubusercontent.com/full-stack-deep-learning/website/main/docs/course/2022/"

  lecture_md_urls = {idx: lecture_md_url_base + title + "/index.md" for idx, title in lecture_titles.items()}

  lecture_md_filenames = [elem for elem in os.listdir("documents") if "lecture" in elem]


  docs_folder = Path("documents")
  lecture_texts = {}


  for fn in lecture_md_filenames:
      idx = int("".join(elem for elem in fn if elem in string.digits))
      lecture_md_path = docs_folder / fn
      with open(lecture_md_path) as f:
          lecture = f.read()
          lecture_texts[idx] = lecture

  from langchain.text_splitter import CharacterTextSplitter


  text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)

  lecture_texts_split = {idx: text_splitter.split_text(lecture_text) for idx, lecture_text in lecture_texts.items()}

  website_url_base = "https://fullstackdeeplearning.com/course/2022/"
  source_urls = {idx: website_url_base + title for idx, title in lecture_titles.items()}
  source_urls_split = {"source": [source_urls[idx]] * len(splits) for idx, splits in lecture_texts_split.items()}

  lecture_texts_flat = [split for lecture_text in lecture_texts_split.values() for split in lecture_text]
  source_urls_flat = [{"source": source_urls[idx]} for idx, lecture_text in lecture_texts_split.items() for split in lecture_text]

  return lecture_texts_flat, source_urls_flat


def embed_texts(texts, metadatas):
  from langchain.embeddings.openai import OpenAIEmbeddings

  embeddings = OpenAIEmbeddings()  # uses ada-002 by default

  from langchain.vectorstores.faiss import FAISS
  # https://github.com/facebookresearch/faiss

  docsearch = FAISS.from_texts(
    texts, embeddings, metadatas=metadatas)

  return docsearch


def make_chain(llm):
  from langchain.chains.qa_with_sources import load_qa_with_sources_chain

  chain = load_qa_with_sources_chain(llm, chain_type="stuff")

  return chain


def run_query(query, chain, docsearch):
  docs = docsearch.similarity_search(query)

  output = chain({"input_documents": docs, "question": query}, return_only_outputs=True)

  return output["output_text"]


if __name__ == "__main__":
  import sys
  go = get_runner()
  print(go(sys.argv[1]))
