# Pocket Aces completion and validation report

Repository: https://github.com/Advaith-Ganesh/Pocket-Aces — branch `main`.
Prepared 7 November 2026. The session deadline is 18:00 Europe/London;
the inspected official repository does not state an event deadline.

## Transfer and provenance

The existing working implementation was found in
`Advaith-Ganesh/poker_bot`, branch `codex/pocketaces-bot`, commit
`44f747b1a251c126a4fd04e976886c289b5a9750`, with a clean working tree.
Its complete Git history and source archive were backed up before changes.
A separate checkout was used for Pocket Aces, and its only push destination
is `Advaith-Ganesh/Pocket-Aces`. The destination was empty when inspected.
The original fork checkout and Manchester AI Society upstream were not changed.

The full engine, arena, evaluation tools, official tests and pinned
requirements are included. Forty-eight upstream runtime/tool/test files
were checked byte-for-byte against official revision
`b852bd52c48cffe0e203b669a07fb198e36fff8e`. The official revision is unchanged
from the earlier implementation. Upstream attribution, notices and history
are retained; no upstream licence file was present. See `ATTRIBUTION.md` and
`docs/ENGINE_README.md`. Historical baseline evidence is in
`docs/BASELINE_REPORT.md` and `docs/BASELINE_VALIDATION.txt`.

The new project README, submission builder, package consistency tests,
comparison helper and .gitignore make the repository usable independently.
No virtual environment, credentials, cache, bulky match log, JavaScript,
TypeScript or compiled project extension is included. No dependency was added.
The existing organiser Pydantic requirement retains its normal native core.
There are no external weights or lookup files: tables are created in `__init__`.

The organisers require **Python 3.10+ for the submitted bot**. Their pinned
`hypothesis==6.170.15` requires **Python 3.11+ for the full test suite**.
`.python-version` selects 3.11 for local development. Dependency pins were
preserved. Original development used Python 3.12. Final checks also passed
on Python 3.10.22 (runtime) and 3.11.17 (full suite); see
`docs/FINAL_CHECKS.md`.

## Contract audit

The actual arena timeout is `arena.remote.TIME_LIMIT = 10.0` seconds per
callback. The bot budgets its decisions to 0.65 seconds with periodic checks.
Vetting permits the team's own modules and explicit data globals, including
`random.Random` and the official `Card`. Initial pickle globals are
`model.Model` and `random.Random`; learned pickles may also name
`card_utils.Card`. Both initial and post-play vetting are exercised.
Only the allowlisted public view is read; no state mutation or hidden
information is used. Only `fold`, `call` or legal integer `raise_to` totals
are returned, and proposed actions and fallbacks are validated.

Source-confirmed types and semantics:

- Seat IDs, player count, chip fields, bets and stack sizes are integers;
  `to_act` can be `None`. Hand/street flags and `can_raise` are booleans.
- The view converts per-player lists, `board`, player-ID collections and
  `legal_actions` to tuples. `street` and team names are strings.
- `raise_range` is an integer pair or `None`; `pot_odds` and `spr` are
  floating-point ratios. `effective_stack` returns chips behind and
  excludes already-bet chips. `pot` includes current street bets.
- `status` returns `active`, `folded` or `all_in`; `validate_action` returns
  normally or raises `InvalidAction`. `legal_actions` is a property.
- Event deltas are consumed once, including `end_game`. Dealer reveals are
  board cards; player reveals are shown hole cards. Seats reset in `seed`,
  while opponent statistics remain keyed by team name.
- Numeric ranks use `Card.value`. The reference and fast evaluators receive
  only 5–7 cards. Simulated holes/runouts exclude known cards, use no
  replacement and split ties. Range caches are bounded and reset per hand.

## Changes supported by evidence

The transferred strategy already used position/depth-aware preflop play,
range-conditioned Monte Carlo equity, pot odds, equity-realisation margins,
board texture, value bets, occasional bluffs and smoothed learning. It was
preserved as the comparison baseline.

One candidate was tested, without a parameter search or model training:
open the remaining weak button hands in actual heads-up games when depth
is at least 12bb, at least 24 responses to preflop raises have been observed,
and the smoothed fold rate exceeds 73%. The prior contributes eight
opportunities at a 55% fold rate. Responses to the blind price alone are
not counted as raise responses. The rule uses observed team behaviour,
not opponent names; it is disabled at larger tables.

Development seeds were **100 and 101**; held-out seeds were **200 and 201**.
Each version used the same decks, duplicate seat rotations and opponent
random seeds. Fold/tight matches used 400 deals per seed (1,600 played hands
per opponent/version); the other opponents used 160 (640 played hands).
No thresholds were changed after inspecting held-out results. The final
version enables this candidate. Counters now separately record budget and
calculation fallbacks plus the last error, so safe fallbacks are inspectable.

All figures below are bb/100 ± 95% confidence half-width. Change intervals
use paired per-deck net differences; individual-version intervals use the
official duplicate scoring. These are uncertainty estimates for fixed toy
opponent policies and deck samples, not bounds on unknown tournament bots.

| Held-out opponent | Existing bot | Final candidate | Paired change | Hands/version |
|---|---:|---:|---:|---:|
| fold | +65.7 ± 1.7 | +74.2 ± 0.5 | +8.5 ± 1.7 | 1,600 |
| call | +313.0 ± 52.5 | +313.0 ± 52.5 | +0.0 ± 0.0 | 640 |
| random | +112.1 ± 52.8 | +112.1 ± 52.8 | +0.0 ± 0.0 | 640 |
| shove | +182.0 ± 95.7 | +182.0 ± 95.7 | +0.0 ± 0.0 | 640 |
| tight | +47.6 ± 9.8 | +55.1 ± 9.6 | +7.5 ± 5.9 | 1,600 |
| equity | +171.7 ± 44.0 | +171.7 ± 44.0 | +0.0 ± 0.0 | 640 |

Both versions recorded zero engine faults throughout this comparison.
Development paired changes were +9.1 ±1.7 against fold and +8.4 ±4.9 against
tight; the other four development matchups also had identical trajectories.
The held-out fold/tight change intervals exclude zero, supporting the
limited exploit. Zero changes against the other opponents are not claims
of stronger play there. Complete compact results, seeds, counts, faults and
timing are in `docs/STRATEGY_COMPARISON.json`.

`compare_versions.py` reproduces paired comparisons from two trusted pickles,
each kept beside its matching sources. Use `--seeds 200 201 --deals 400
--opponents fold tight`; use 160 deals for call/random/shove/equity. Baseline
source is retained in Git at commit `44f747b`. Keep development and held-out
deals disjoint. The comparison helper was smoke-checked by comparing an
identical baseline pickle against itself: zero paired difference and faults.

## Final verification

The final model was frozen before the following checks. A development run
started during editing initially mixed an old pickle and updated worker
source and failed with a missing setting (4 failed, 5 passed). The cause was
identified; validation was restarted on a consistent source version. The
final build regenerates the pickle, clean-worker validation checks loading,
and package tests require ZIP/manifest/source agreement. This development
failure is distinct from the zero faults in final matches.

- `.venv/bin/python -m pytest tests/test_model.py -q`: **9 passed in 12.77 s**.
- `.venv/bin/python -m pytest tests test_bot.py test_submission.py -q`:
  **439 passed, 5 skipped in 122.65 s**. Official tests were not modified.
- `.venv/bin/python build_submission.py`: actual organiser vetting found
  no source findings/refused globals, and clean-worker play passed every dummy.
- A separate 120-hand run covered 2/3/6/9 players, swapped seats/buttons,
  stacks from 7 to 2,000 chips and pickle round trips after every hand.
  It recorded **0 faults, 0 internal fallbacks**, and a slowest decision of
  **0.08181 s**. Its learned pickle also passed actual organiser vetting.
- A synthetic nine-player/256-observation stress test intentionally exhausted
  the budget: **0.65268 s**, legal check, one budget fallback, zero calculation
  fallbacks. The recorded reason was `range budget exhausted`. This is an
  expected safety fallback, not an engine fault or a normal match result.
- The evaluator matched the reference on 2,000 new seven-card samples;
  reference **124.494 µs/hand**, fast evaluator **4.623 µs/hand** (26.93x in
  this measurement). The regression suite separately checks 3,600 random
  5/6/7-card hands plus explicit wheel, flush, quads, full-house and pair cases.
- Actual execution used Python 3.12, satisfying both the organiser's 3.10+
  runtime requirement and the test suite's 3.11+ dependency minimum.
  Dependency metadata was checked, including Hypothesis.
- The final staged files were reviewed, with no credential-pattern matches,
  caches, virtual environments or generated match logs included. The full
  original commit history is retained for provenance.

### Smoke evaluation

`.venv/bin/python -m evals --deals 40` completed with zero faults against
all six dummies (80 played hands per opponent). The shove and equity
intervals crossed zero; this was a smoke check, not evidence of strength.

### Default evaluation

`.venv/bin/python -m evals` completed with 500 duplicate deals per opponent,
1,000 played hands each, seed 0. Figures are bb/100 ± 95% half-width:

```text
opponents                       your bb/100  verdict   hands faults  slowest
fold                         +74.4 ± 0.6       ahead    1000      0    0.03s
call                        +283.7 ± 40.4      ahead    1000      0    0.27s
random                      +124.6 ± 44.6      ahead    1000      0    0.08s
shove                       +161.6 ± 78.1      ahead    1000      0    0.02s
tight                        +49.5 ± 14.9      ahead    1000      0    0.06s
equity                      +179.8 ± 35.0      ahead    1000      0    0.09s
```

### Requested longer evaluation

`.venv/bin/python -m evals --opponents tight equity --deals 1000 --table`
completed at seed 0. Heads-up matches have 2,000 played hands each and the
three-player table has 3,000:

```text
opponents                       your bb/100  verdict   hands faults  slowest
tight                        +55.5 ± 9.8       ahead    2000      0    0.11s
equity                      +163.4 ± 24.4      ahead    2000      0    0.16s
table of 3                   +82.6 ± 19.0      ahead    3000      0    0.09s
```

All requested final evaluations recorded **zero engine faults**. The
slowest match callback across the final evaluation commands was **0.27 s**,
well below the actual 10 s limit. Scenario checks separately measured zero
internal fallbacks; evaluation fault totals alone should not be interpreted
as a direct count of internal fallbacks.

## Exact submission and reproduction

From the repository root, after installing the documented development
requirements under Python 3.11+:

```sh
.venv/bin/python -m pytest tests/test_model.py -q
.venv/bin/python -m pytest tests test_bot.py test_submission.py -q
.venv/bin/python -m evals
.venv/bin/python -m evals --opponents tight equity --deals 1000 --table
.venv/bin/python build_submission.py
```

The canonical upload files are:

- `submission/pocketaces.pkl`
- `submission/model.py`
- `submission/poker_eval.py`

`submission/pocketaces-submission.zip` contains exactly those three basenames,
verified against the root sources and `submission/manifest.json`. The package
contains a newly constructed Model with empty opponent history, rather than
an instance trained on the evaluation opponents. Module names remain exactly
`model` and `poker_eval`; no unsubmitted data or weights are required.
The builder uses the organiser's clean staging and fresh-process import path.

The live form was checked again and still asks for a repository link and
team/member/email fields. Paste `https://github.com/Advaith-Ganesh/Pocket-Aces`
and follow the root README. The form has not been submitted.

### Package SHA-256

```text
db52b95c1e91ae249b29964fc8fea8080a8650f81e84ac0e8c423ef42a5d3663  submission/pocketaces.pkl
d6bee639738e6dca071e3fa55edd46879ec178cbcdd7a5d5f2627bc50860f4ac  submission/model.py
78a59bb3311d769355e18f578d3482ce773a22577035047a978107b57bbd59ec  submission/poker_eval.py
de12e0b70b20d4818900616950f526fafc88ae81da12c803eb98cb5b2e9e1a6f  submission/pocketaces-submission.zip
```

## Limitations and blockers

There is no remaining implementation, validation or packaging blocker.
The bot uses heuristic ranges, finite sampling and approximate multiway
side-pot valuation. The new adaptation was validated only on the stated
opponent policies and independent deck seeds; it does not establish
improvement against unknown tournament bots. No tournament win is promised.
The submitted bot follows the organiser's Python 3.10+ requirement. Local
development uses Python 3.11+ for the unchanged Hypothesis pin; execution
was verified on 3.10.22, with full suites passing on 3.11.17 and 3.12
(see `docs/FINAL_CHECKS.md`).
The event deadline comes from this session because upstream
does not state one. User submission of the form remains required.
