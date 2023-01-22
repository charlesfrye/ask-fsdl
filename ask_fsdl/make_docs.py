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

    import srt

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

    srt_filenames = list(sorted([elem for elem in os.listdir(docs_folder) if elem.endswith(".srt")]))
    srt_urls = get_srt_urls()
    srt_texts_flat, srt_metadatas_flat = [], []

    for fn in srt_filenames:
        idx = int("".join(elem for elem in fn if elem in string.digits))
        srt_url = srt_urls[idx]

        srt_text_path = docs_folder / fn
        with open(srt_text_path) as f:
            srt_text = "\n".join(f.readlines())

        subtitles = list(srt.parse(srt_text))

        texts, metadatas = create_srt_texts_and_metadatas(subtitles, srt_url)
        srt_texts_flat += texts
        srt_metadatas_flat += metadatas

    texts_flat = lecture_texts_flat + srt_texts_flat
    metadatas_flat = source_urls_flat + srt_metadatas_flat

    return texts_flat, metadatas_flat


def create_srt_texts_and_metadatas(subtitles, base_url):
    query_params_format = "&t={start}s"
    texts, metadatas = [], []

    for subtitle in subtitles:
        raw_text = subtitle.content
        text = subtitle.content.strip()
        start = timestamp_from_timedelta(subtitle.start)
        url = base_url + query_params_format.format(start=start)

        texts.append(text)
        metadatas.append({"source": url})

    return texts, metadatas


def timestamp_from_timedelta(timedelta):
    return int(timedelta.total_seconds())


def get_srt_urls():
    return {
        1: "https://www.youtube.com/watch?v=-Iob-FW5jVM",
        2: "https://www.youtube.com/watch?v=BPYOsDCZbno",
        3: "https://www.youtube.com/watch?v=RLemHNAO5Lw",
        4: "https://www.youtube.com/watch?v=Jlm4oqW41vY",
        5: "https://www.youtube.com/watch?v=W3hKjXg7fXM",
        6: "https://www.youtube.com/watch?v=nra0Tt3a-Oc",
        7: "https://www.youtube.com/watch?v=Rm11UeGwGgk",
        8: "https://www.youtube.com/watch?v=a54xH6nT4Sw",
        9: "https://www.youtube.com/watch?v=7FQpbYTqjAA"
        }


if __name__ == "__main__":
  download_lectures()
  texts, metadatas = produce_documents()
  print(texts[-1])
  print(metadatas[-1])
