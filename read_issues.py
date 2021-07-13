# %%
import json
import os
from github import Github
import time
from decouple import config

githubApiToken = config('githubApiToken', default='')

g = Github(githubApiToken)
repos = ['expressjs/express', 'facebook/react',
         'microsoft/TypeScript', 'prisma/prisma',
         'tensorflow/tensorflow', 'tailwindlabs/tailwindcss',
         'vercel/next.js', 'arangodb/arangodb']

# %%
for repo in repos:
    print('starting with: ', repo)
    file_name = 'issues/' + repo.split('/')[1] + '.json'

    if os.path.exists(file_name):
        continue

    data = []

    repo_issues = g.get_repo(repo).get_issues(state='all')

    check_rate_limit = 100
    for count, issue in enumerate(repo_issues):
        check_rate_limit -= 1

        if issue.pull_request == None:
            data.append({'name': 'Issue ' + str(issue.number),
                        "url": str(issue.html_url), "title": str(issue.title), "body": str(issue.body), "label": None})

        if check_rate_limit < 10:
            while g.get_rate_limit().raw_data['core']['remaining'] < 150:
                print('wait to continue (rate limit)')
                time.sleep(300)
            check_rate_limit = 100

        print('finished issue: ' + str(count) +
              '/' + str(repo_issues.totalCount))

    with open(file_name, 'w') as write_obj:
        json.dump(data, write_obj)

# %%
