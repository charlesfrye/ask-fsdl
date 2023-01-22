from pathlib import Path

DOCS_FOLDER = Path("documents")

def download_lectures(docs_folder=DOCS_FOLDER):
    import os
    import subprocess

    if not os.path.exists(docs_folder):
        os.makedirs(docs_folder, exist_ok=True)

    lecture_titles = get_lecture_titles()
    lecture_md_urls = list_lecture_md_urls(lecture_titles)

    for idx, url in lecture_md_urls.items():
        filename = "documents/lecture-{}.md".format(str(idx).zfill(2))
        if not os.path.exists(filename):
          subprocess.run(["wget","-O", filename, url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def list_lecture_md_urls(lecture_titles):

    lecture_md_url_base = "https://raw.githubusercontent.com/full-stack-deep-learning/website/main/docs/course/2022/"

    lecture_md_urls = {idx: lecture_md_url_base + title + "/index.md" for idx, title in lecture_titles.items()}

    return lecture_md_urls


def get_lecture_titles():
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

    return lecture_titles


def produce_documents(docs_folder=DOCS_FOLDER):
    """Assumes the documents are on disk already."""
    import os
    from pathlib import Path
    import shutil
    import string

    if not os.path.exists(docs_folder):
        os.makedirs(docs_folder, exist_ok=True)

    lecture_md_filenames = [elem for elem in os.listdir(docs_folder) if "lecture" in elem]

    lecture_titles = get_lecture_titles()
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


if __name__ == "__main__":
  download_lectures()
  print(produce_documents()[0])
