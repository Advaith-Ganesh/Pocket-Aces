"""Build, vet and clean-process validate the upload bundle.

Run from the repository root: .venv/bin/python build_submission.py
This development tool is not part of the submitted bot.
"""

import hashlib
import json
from pathlib import Path
import shutil
import zipfile

from arena import vet
from submit import local_modules, main as submit_main


def main():
    root = Path(__file__).resolve().parent
    if Path.cwd().resolve() != root:
        raise SystemExit('Run build_submission.py from the repository root.')
    target = root / 'submission'
    target.mkdir(exist_ok=True)
    result = submit_main(['--team', 'pocketaces', '--out', str(target)])
    if result:
        return result
    pickle_path = target / 'pocketaces.pkl'
    globals_ = vet.pickle_globals(str(pickle_path))
    modules = {name.rpartition('.')[0].split('.')[0] for name in globals_}
    sources = local_modules(modules, str(root))
    files = [pickle_path]
    for source in sources:
        destination = target / Path(source).name
        shutil.copyfile(source, destination)
        files.append(destination)
    report = vet.vet(str(pickle_path), [str(path) for path in files[1:]])
    if not report.ok:
        raise SystemExit('\n'.join(report.lines()))
    checksums = {path.name: hashlib.sha256(path.read_bytes()).hexdigest()
                 for path in files}
    (target / 'manifest.json').write_text(
        json.dumps({'team': 'PocketAces', 'pickle_protocol': 4,
                    'files': checksums}, indent=2) + '\n', encoding='utf-8')
    # Stable ZIP metadata avoids platform-specific timestamps/permissions.
    with zipfile.ZipFile(target / 'pocketaces-submission.zip', 'w') as archive:
        for path in files:
            info = zipfile.ZipInfo(path.name, (2026, 11, 7, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, path.read_bytes())
    print('\nVerified upload bundle: submission/pocketaces-submission.zip')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
