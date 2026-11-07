# PocketAces upload files

Organiser's bot requirement: **Python 3.10+**. The local development/test
environment uses Python 3.11+ for the official test dependency.

This directory is generated from the repository-root bot by:

```sh
.venv/bin/python build_submission.py
```

The script uses the organiser's `submit.py`, actual vetting rules and a
clean worker containing only the required submission sources and pickle.

Submit these **three files together**:

- `pocketaces.pkl`
- `model.py`
- `poker_eval.py`

`pocketaces-submission.zip` contains exactly those files. Extract it if
individual uploads are requested. `manifest.json` records their SHA-256
checksums; neither this README nor the manifest is required to load the bot.

The live form currently asks for a GitHub repository link. Use
`https://github.com/Advaith-Ganesh/Pocket-Aces`, which includes this directory,
the complete runnable project and matching root-level bot sources.
See the root README for the form link and steps. Do not rename the Python
modules: the pickle expects `model.Model`. No external tables or weights
are required.
