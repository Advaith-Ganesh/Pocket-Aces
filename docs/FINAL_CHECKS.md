# Final tournament readiness checks

Completed 7 November 2026, before the 18:00 Europe/London session deadline.
Checked the published bot at commit `b156fd99171a82d2308fe2a0e2062c7dd4f980aa`
in a fresh clone. No strategy or submission-source changes were needed.

## Python and language compatibility

- **Python 3.10.22:** installed only the organiser's runtime requirements and
  loaded the actual published pickle, created earlier on Python 3.12.
  Fresh arena-worker play, package checks and post-play pickling all passed.
- **Python 3.11.17:** installed the exact development requirements; the full
  official and added suite passed: **439 passed, 5 skipped in 79.03 s**.
- **Python 3.12:** repeated the full suite: **439 passed, 5 skipped in 81.09 s**.
- The organiser's bot requirement remains **Python 3.10+**. Their pinned
  Hypothesis requires **3.11+ only for the full development test suite**.
  `.python-version` selects 3.11 for local development and is not part of
  the uploaded bot. No Python 3.11 runtime guard was added to the bot.
- GitHub's language API reports **Python only**. There are no JavaScript,
  TypeScript or compiled project extensions in the tracked source.

## Actual Python 3.10 runtime checks

The published pickle ran against every official dummy in fresh worker
processes, plus full-table and short-stack matches, using the actual
10-second arena timeout:

| Match | Played hands | Bot faults | Slowest decision |
|---|---:|---:|---:|
| fold | 60 | 0 | 0.000 s |
| call | 60 | 0 | 0.129 s |
| random | 60 | 0 | 0.074 s |
| shove | 60 | 0 | 0.019 s |
| tight | 60 | 0 | 0.078 s |
| equity | 60 | 0 | 0.126 s |
| table-6, stack-500 | 72 | 0 | 0.046 s |
| table-4, stack-60 | 80 | 0 | 0.032 s |

That is **512 worker-process hands with zero faults**. A further **120
scenario hands** used 2/3/6/9 players, shuffled seats/buttons, stacks from
7 to 2,000 chips and a pickle round trip after every hand:

- All four streets were exercised.
- Observed actions: 38 folds, 75 calls and 48 raises, including 44 checks,
  26 short-stack calls and 10 all-in raises.
- There were 47 decisions with raising unavailable.
- **Zero engine faults and zero internal fallbacks**.
- Learned-model pickle passed actual organiser vetting with no findings.
- Slowest decision across these Python 3.10 checks: **0.139 s**, versus the
  **10.0 s** callback limit.

These are compatibility and integration checks, not fresh claims about
playing strength. The larger strength evaluations and their confidence
intervals remain in `REPORT.md`.

## Submission and engine integrity

- ZIP contents are exactly `pocketaces.pkl`, `model.py`, `poker_eval.py`.
- Every checksum matches `submission/manifest.json`; packaged Python
  sources match the repository-root bot sources byte for byte.
- The pickle contains a fresh model with empty opponent history.
- The actual source and pickle vetting passed; public-view attribute reads
  match the organiser's whitelist.
- Official engine, arena, evaluation opponents, tests and requirement pins
  remain unchanged. The live upstream HEAD was rechecked and is still
  `b852bd52c48cffe0e203b669a07fb198e36fff8e`.
- Bot runtime uses no network/API calls or unsubmitted files.

### Verified upload files

```text
submission/pocketaces.pkl
submission/model.py
submission/poker_eval.py
```

Convenience bundle: `submission/pocketaces-submission.zip`.

SHA-256:

```text
db52b95c1e91ae249b29964fc8fea8080a8650f81e84ac0e8c423ef42a5d3663  submission/pocketaces.pkl
d6bee639738e6dca071e3fa55edd46879ec178cbcdd7a5d5f2627bc50860f4ac  submission/model.py
78a59bb3311d769355e18f578d3482ce773a22577035047a978107b57bbd59ec  submission/poker_eval.py
de12e0b70b20d4818900616950f526fafc88ae81da12c803eb98cb5b2e9e1a6f  submission/pocketaces-submission.zip
```

The bot passes the current organiser engine's compatibility, loading,
legality and timing checks. There is no known submission blocker. Tournament
placing depends on the other bots; no win is guaranteed. The tournament form
has not been submitted by the assistant.
