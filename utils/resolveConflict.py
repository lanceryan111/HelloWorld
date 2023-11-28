import re
import sys
from pathlib import Path

def resolve_conflict(head, theirs, match_string):
    if '"version":' not in head and 'projectVersion=' not in head:
        raise ValueError("Found non-version related conflict, exiting auto resolution")
    return head

def main():
    _, _, file, overwrite = sys.argv

    source_text = Path(file).read_text()

    lend = r'(\n|\r\n)'  # Support cross-platform line endings
    pattern = re.compile(
        f'<<<<<<< HEAD{lend}(?P<head>.*?){lend}======='
        f'{lend}(?P<theirs>.*?){lend}>>>>>>> (?P<branchName>[^{lend}]+)',
        re.DOTALL | re.MULTILINE
    )

    result_text = source_text
    resolved_count = 0
    total_count = 0
    replacements = []

    for match in pattern.finditer(source_text):
        print(match.group(0))
        groups = match.groupdict()
        head, theirs, branch_name = groups['head'], groups['theirs'], groups['branchName']
        match_string = match.group(0)
        replacement_string = resolve_conflict(head, theirs, match_string)

        if replacement_string:
            replacements.append((match.start(), match.end(), replacement_string))
            resolved_count += 1

        total_count += 1
        print('branchName:      ', branch_name)
        print('head:            ', head)
        print('theirs:          ', theirs)
        print('matchString:     ', match_string)
        print('replacementString:', replacement_string)
        print('--------------------')

        result_text = result_text.replace(match_string, replacement_string, 1)

    if len(replacements) > 1:
        raise ValueError('Found multiple conflicts, exiting auto resolution')

    if overwrite:
        print('Overwriting file.')
        Path(file).write_text(result_text)
    else:
        print('Dry run (Not overwriting file).')
        print(result_text)

    print('Resolved %d out of %d conflicts.' % (resolved_count, total_count))

if __name__ == "__main__":
    main()
