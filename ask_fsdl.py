def setup():
  print("TODO: put setup in a function, you slob")

###
# PREPARE LLM
###

from dotenv import load_dotenv

load_dotenv()

from langchain.llms import OpenAI

davinci_003 = OpenAI(temperature=0., model_name="text-davinci-003")

###
# PREPARE DOCUMENTS
###

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

print("TODO: actually dl the docs")

import os

lecture_md_filenames = [elem for elem in os.listdir("documents") if "lecture" in elem]


import string
from pathlib import Path


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


from langchain.embeddings.openai import OpenAIEmbeddings  # TODO: read the API docs here


embeddings = OpenAIEmbeddings()  # uses ada-002 by default


website_url_base = "https://fullstackdeeplearning.com/course/2022/"
source_urls = {idx: website_url_base + title for idx, title in lecture_titles.items()}
source_urls_split = {"source": [source_urls[idx]] * len(splits) for idx, splits in lecture_texts_split.items()}

lecture_texts_flat = [split for lecture_text in lecture_texts_split.values() for split in lecture_text]
source_urls_flat = [{"source": source_urls[idx]} for idx, lecture_text in lecture_texts_split.items() for split in lecture_text]

from langchain.vectorstores.faiss import FAISS  # TODO: what is this?
# https://github.com/facebookresearch/faiss

docsearch = FAISS.from_texts(
  lecture_texts_flat, embeddings, metadatas=source_urls_flat)


###
# CREATE CHAIN
###
from langchain.chains.qa_with_sources import load_qa_with_sources_chain

chain = load_qa_with_sources_chain(davinci_003, chain_type="stuff")

def run_query(query):
  docs = docsearch.similarity_search(query)

  output = chain({"input_documents": docs, "question": query}, return_only_outputs=True)

  return output["output_text"]
