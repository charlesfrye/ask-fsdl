import ask_fsdl


if __name__ == "__main__":
  import sys

  ask_fsdl.make_docs.download_lectures()

  runner = ask_fsdl.get_runner()

  print(runner(sys.argv[1]))
