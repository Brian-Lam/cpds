import os
from pprint import pprint

# _dir = os.walk('.')
# folders = [ _name for _name in os.listdir(_dir) if os.path.isdir(os.path.join(_dir, _name)) ]
# pprint(folders)
print(os.listdir(os.getcwd() + "/repositories"))