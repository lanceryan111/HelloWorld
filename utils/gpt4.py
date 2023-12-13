```python
import re
import sys
from pathlib import Path

def resolve_conflict(head):
    if '"version":' not in head and 'projectVersion=' not in head:
        raise ValueError("Found non-version related conflict, exiting auto resolution")
    return head

def main():
    if len(sys.argv) < 3:
        print("Usage: script.py <file> <overwrite>")
        sys.exit(1)

    file_path = sys.argv[1]
    overwrite = sys.argv[2].lower() == 'true'

    source_text = Path(file_path).read_text()

    pattern = r'<<<<<<< HEAD(\n|\r\n)(?P<head>.*?)(\n|\r\n)=======(\n|\r\n)(?P<theirs>.*?)(\n|\r\n)>>>>>>> (?P<branchName>[^\n\r]+)'
    regex = re.compile(pattern, re.DOTALL | re.MULTILINE)

    result_text = source_text
    resolved_count = 0
    total_count = 0
    replacements = []

    for match in regex.finditer(source_text):
        print(match.group(0))
        head, theirs, branch_name = match.group('head', 'theirs', 'branchName')
        replacement_string = resolve_conflict(head)
        if replacement_string:
            replacements.append((match.start(), match.end(), replacement_string))
            result_text = result_text[:match.start()] + replacement_string + result_text[match.end():]
            resolved_count += 1
        total_count += 1

        print('branchName: ', branch_name)
        print('head: ', head)
        print('theirs: ', theirs)
        print('matchString: ', match.group(0))
        print('replacementString:', replacement_string)
        print('--------------------')

    if len(replacements) > 1:
        raise ValueError('Found multiple conflicts, exiting auto resolution')

    if overwrite:
        print('Overwriting file.')
        Path(file_path).write_text(result_text)
    else:
        print('Dry run (Not overwriting file).')
        print(result_text)

    print(f'Resolved {resolved_count} out of {total_count} conflicts.')

if __name__ == "__main__":
    main()
```
