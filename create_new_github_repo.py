import os
from github import Github
TOCKEN = os.getenv('PERSONAL_TOCKEN')
g = Github('pydemo',TOCKEN)
repo = g.get_user().user.create_repo("your-new-repos-name")