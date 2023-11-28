import subprocess
import requests

def is_first_branch_newer(branch1, branch2):
    # Implement the logic for comparing branches
    # Return True if branch1 is newer than branch2, else False
    pass

current_branch = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD']).decode('utf-8').strip()

print('currentBranch', current_branch)

if current_branch == 'develop' or not current_branch.startswith('release/'):
    print('Clean exit')
    exit()

current_version = current_branch[current_branch.index('/') + 1:].strip()

all_branches = subprocess.check_output(['git', 'branch', '-r']).decode('utf-8').splitlines()

all_other_release_branch_versions = [
    branch[branch.index('/') + 1:].strip() for branch in all_branches
    if branch.startswith('origin/release/')
    and branch[branch.index('/') + 1:].strip() != current_version
]

all_other_tokenized_release_branch_versions = [
    {'version': version, 'tokens': version.split(/[_\-+.]+/)} for version in all_other_release_branch_versions
]

tokenized_current_version = {'version': current_version, 'tokens': current_version.split(/[_\-+.]+/)}

tokenized_next_version = next(
    (
        version for version in all_other_tokenized_release_branch_versions
        if is_first_branch_newer(version, tokenized_current_version)
    ),
    None
)

next_branch = 'develop' if not tokenized_next_version else f"release/{tokenized_next_version['version']}"
print('nextBranch', next_branch)

# First create a new branch off our current branch
pr_branch_name = f"feature/merge-conflict-{tokenized_current_version['version']}-to-{tokenized_next_version['version'] if tokenized_next_version else 'develop'}"
subprocess.run(['git', 'checkout', '-b', pr_branch_name])

# Next checkout our target next branch
subprocess.run(['git', 'checkout', f'--track origin/{next_branch}'])

has_conflict = False
requires_pr = False

try:
    print('\n=== Starting Merge ===\n')
    subprocess.run(['git', 'merge', current_branch], check=True, text=True)
    subprocess.run(['git', 'push', 'origin', next_branch], check=True, text=True)
except subprocess.CalledProcessError:
    has_conflict = True
    requires_pr = True

if has_conflict:
    print('\n=== Attempting to resolve conflicts ===\n')
    try:
        target_file_matches = ['package.json', 'sonar-project.properties']
        conflict_buffer = subprocess.check_output(['git', 'diff', '--name-only', '--diff-filter=U']).decode('utf-8')
        conflict_files = conflict_buffer.strip().split('\n')
        for file_path in conflict_files:
            if any(file_path.endswith(target_match) for target_match in target_file_matches):
                source_file_name = file_path
                tmp_file_name = f"{file_path}.tmp"
                subprocess.run(['mv', source_file_name, tmp_file_name])
                subprocess.run(['python', './utils/resolveVersionConflict.py', tmp_file_name, 'true'], check=True, text=True)
                subprocess.run(['mv', tmp_file_name, source_file_name])
                subprocess.run(['git', 'add', source_file_name], check=True, text=True)

        conflicts = subprocess.check_output(['git', 'diff', '--check'], text=True)
        if conflicts:
            raise RuntimeError('There are still conflicts remaining.')

        subprocess.run(['git', 'commit', '-m', f"Merge branch '{current_branch}' into {next_branch}"], check=True, text=True)
        subprocess.run(['git', 'push', 'origin', next_branch], check=True, text=True)
        requires_pr = False
    except subprocess.CalledProcessError as e:
        print(e)
        requires_pr = True

if requires_pr:
    print('\n=== PR is required ===\n')
    subprocess.run(['git', 'push', 'origin', pr_branch_name], check=True, text=True)
    headers = {'Authorization': f'token {os.environ["GH_TOKEN"]}'}
    data = {'title': f"chore: merge '{current_branch}' into {next_branch}", 'head': pr_branch_name, 'base': next_branch}
    requests.post('https://api.github.com/repos/jrparish/cascading-merge/pulls', json=data, headers=headers)

print('\n=== Cascade complete ===\n')
