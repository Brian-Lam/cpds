import os
import sys

def walk(extension = ".php"):
  _dir = os.getcwd() + "/repositories"
  for root, dirs, files in os.walk(_dir):
      for file in files:
          if file.endswith(extension):
               print(os.path.join(root, file))

if __name__ == "__main__":
  if (len(sys.argv) > 1):
    walk(sys.argv[1])
