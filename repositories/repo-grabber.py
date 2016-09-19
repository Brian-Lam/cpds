import subprocess
from pprint import pprint
from repoauth import _user, _password
import json
import os
from Queue import Queue
from threading import Thread


WORKER_THREADS = 30

# Get credentials from repoauth
credentials = _user + ":" + _password

# Save repo data to file
f = open("repos", "w")
subprocess.call(["curl", "-u", credentials, "https://bitbucket.org/api/1.0/user/repositories/"], stdout=f)

# Parse repos JSON data
with open("repos") as data_file:    
  repos = json.load(data_file)

# Thread queue for multiprocessed cloning
q = Queue()

# Clone repo process called by worker thread
def cloneRepo(owner, slug):
	print(owner + " " + slug)
	url = "git@bitbucket.org:" + owner + "/" + slug + ".git"
	if not (os.path.exists(slug)):
		subprocess.call(["git", "clone", url])

# Worker thread - retrieve from Queue and process data for cloning
def worker():
    while True:
        repoData = q.get()
        cloneRepo(repoData[0], repoData[1])
        q.task_done()


# Create Worker Threads
for i in range(WORKER_THREADS):
     t = Thread(target=worker)
     t.daemon = True
     t.start()

# Populate queue with repo data for cloning
for repo in repos:
	owner = repo["owner"]
	slug = repo["slug"]
	q.put((owner, slug))

# block until all tasks are done
q.join()       
  
## Clear out media and document files
subprocess.call("find . -type f -iname \*.jpg -delete", shell=True)
subprocess.call("find . -type f -iname \*.png -delete", shell=True)
subprocess.call("find . -type f -iname \*.gif -delete", shell=True)
subprocess.call("find . -type f -iname \*.pdf -delete", shell=True)
subprocess.call("find . -type f -iname \*.mp3 -delete", shell=True)
subprocess.call("find . -type f -iname \*.mp4 -delete", shell=True)
subprocess.call("find . -type f -iname \*.docx -delete", shell=True)
subprocess.call("find . -type f -iname \*.doc -delete", shell=True)
subprocess.call("find . -type f -iname \*.exe -delete", shell=True)
subprocess.call("find . -type f -iname \*.pdb -delete", shell=True)
subprocess.call("find . -type f -iname \*.DS_Store -delete", shell=True);
subprocess.call("find . -name 'node_modules' -exec rm -r '{}' \;", shell=True)
