import subprocess
from pprint import pprint
from repoauth import _user, _password
import json
import os

f = open("repos", "w")

credentials = _user + ":" + _password
subprocess.call(["curl", "-u", credentials, "https://bitbucket.org/api/1.0/user/repositories/"], stdout=f)

with open("repos") as data_file:    
  repos = json.load(data_file)

for repo in repos:
  owner = repo["owner"]
  slug = repo["slug"]
  print(owner + " " + slug)
  url = "git@bitbucket.org:" + owner + "/" + slug + ".git"
  if not (os.path.exists(slug)):
    subprocess.call(["git", "clone", url])
    subprocess.call("find . -type f -iname \*.jpg -delete", shell=True);
    subprocess.call("find . -type f -iname \*.png -delete", shell=True);
    subprocess.call("find . -type f -iname \*.gif -delete", shell=True);
    subprocess.call("find . -type f -iname \*.pdf -delete", shell=True);
    subprocess.call("find . -type f -iname \*.mp3 -delete", shell=True);
    subprocess.call("find . -type f -iname \*.mp4 -delete", shell=True);
    subprocess.call("find . -type f -iname \*.docx -delete", shell=True);
    subprocess.call("find . -type f -iname \*.doc -delete", shell=True);
    subprocess.call("find . -type f -iname \*.exe -delete", shell=True);
    subprocess.call("find . -type f -iname \*.pdb -delete", shell=True);
    subprocess.call("find . -name 'node_modules' -exec rm -r '{}' \;", shell=True)