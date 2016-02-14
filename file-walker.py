import os
import sys

def walk(substring = ".php"):
  _dir = os.getcwd() + "/repositories"
  for root, dirs, files in os.walk(_dir):
      for file in files:
          path = os.path.join(root, file)
          if substring in path:
              if not ".git" in path:
               print(path)

def printUsage():
  print "USAGE:"
  print "python file-walker.py [substring]"
  print "  Grab files whose full path contains the given substring, such as 'spring2015-module1'"

if __name__ == "__main__":
  if (len(sys.argv) > 1):
    walk(sys.argv[1])
  else:
    printUsage()
