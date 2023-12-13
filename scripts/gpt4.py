import os
import subprocess
import requests

def exec_sync(command):
    return subprocess.run(command, stdout=subprocess.PIPE, text=True, shell=True).stdout.strip()

def create_pull_request(current_branch, next_branch, pr_branch_name):
    url = 'https://api.github.com/repos/jrparish/cascading-merge/pulls'
    headers = {'Authorization': f'token {os.getenv("GH_TOKEN")}'}
    payload = {
        'title': f'chore: merge \'{current_branch}\' into {next_branch}',
        'head': pr_branch_name,
        'base': next_branch
    }
    response = requests.post(url, json=payload, headers=headers)
    return response

current_branch = exec_sync('git rev-parse --abbrev-ref HEAD')
print('currentBranch', current_branch)

if current_branch == 'develop' or not current_branch.startswith('release/'):
    print('Clean exit')
    exit()

current_version = current_branch.split('/')[1]

all_branches = exec_sync('git branch -r').splitlines()
all_other_release_branch_versions = [
    branch.split('/')[1]
    for branch in all_branches
    if branch.startswith('release/') and branch.split('/')[1] != current_version
]

# Insert logic for isFirstBranchNewer here
# ...

next_branch = 'develop'
# ...

print('nextBranch', next_branch)

exec_sync(f'git checkout -b {pr_branch_name}')
exec_sync(f'git checkout --track origin/{next_branch}')

has_conflict = False
requires_pr = False

try:
    print('\n=== Starting Merge ===\n')
    exec_sync(f'git merge {current_branch}')
    exec_sync(f'git push origin {next_branch}')
except Exception as e:
    has_conflict = True
    requires_pr = True

if has_conflict:
    print('\n=== Attempting to resolve conflicts ===\n')
    # Insert logic for resolving conflicts here
    # ...

if requires_pr:
    print('\n=== PR is required ===\n')
    exec_sync(f'git push origin {pr_branch_name}')
    create_pull_request(current_branch, next_branch, pr_branch_name)

print('\n=== Cascade complete ===\n')
