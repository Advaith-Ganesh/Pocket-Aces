"""Regression checks against stale sources or incomplete upload bundles."""

import hashlib
import json
from pathlib import Path
import zipfile

from arena import vet


ROOT = Path(__file__).resolve().parent


def test_submission_matches_current_source_and_manifest():
    folder = ROOT / 'submission'
    manifest = json.loads((folder / 'manifest.json').read_text())
    assert set(manifest['files']) == {'pocketaces.pkl', 'model.py', 'poker_eval.py'}
    for name, expected in manifest['files'].items():
        data = (folder / name).read_bytes()
        assert hashlib.sha256(data).hexdigest() == expected
        if name.endswith('.py'):
            assert data == (ROOT / name).read_bytes()
    with zipfile.ZipFile(folder / 'pocketaces-submission.zip') as archive:
        assert set(archive.namelist()) == set(manifest['files'])
        for name in archive.namelist():
            assert archive.read(name) == (folder / name).read_bytes()


def test_actual_organiser_vetting_of_upload_files():
    folder = ROOT / 'submission'
    report = vet.vet(str(folder / 'pocketaces.pkl'),
                     [str(folder / 'model.py'), str(folder / 'poker_eval.py')])
    assert report.ok, report.lines()
    assert set(report.pickle_globals) == {'model.Model', 'random.Random'}
