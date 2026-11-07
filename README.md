# Pocket Aces

Pocket Aces is our Python poker bot for the **Manchester AI Society / MUDS
AI hackathon**. It plays heads-up no-limit Texas Hold'em using position-aware
preflop choices, range-weighted Monte Carlo equity, stack/pot-aware betting
and conservative opponent learning. It also supports larger tables safely.

The poker engine, arena and official evaluation tools are upstream Manchester
AI Society code. The bot lives in `model.py` and `poker_eval.py`; see
[ATTRIBUTION.md](ATTRIBUTION.md) for provenance and the unchanged upstream
revision. This repository contains everything needed to develop, evaluate
and package the bot. No frontend or external training service is required.

## Setup

**Python 3.11+ is required** for this project (3.12 was tested).
Run commands from this repository's root:

```sh
python3.11 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
```

On Windows use `.venv\Scripts\python` and `.venv\Scripts\pip`. Runtime
requirements remain the organiser's exact `pydantic==2.14.3`; development
adds only the pinned pytest and Hypothesis tools. The bot itself uses only
Python's standard library plus the official interfaces. No compiled
extension or dependency was added; the organiser's existing Pydantic
installation includes its normal `pydantic-core` dependency.

## Test and measure

```sh
.venv/bin/python -m pytest tests/test_model.py -q
.venv/bin/python -m pytest tests test_bot.py test_submission.py -q
.venv/bin/python -m evals --deals 40
.venv/bin/python -m evals
.venv/bin/python -m evals --opponents tight equity --deals 1000 --table
```

The first test runs the pickled model in fresh arena workers against every
official dummy. The added tests check event deltas, legal actions, swapped
seats, short stacks, range sampling, ties and package/source consistency.
A smoke match establishes basic operation; it does not establish strength.
Evaluation output reports bb/100, 95% intervals, played hands, faults and
slowest callbacks. Duplicate heads-up deals run once per seat: 1,000 deals
means 2,000 played hands. See [REPORT.md](REPORT.md) for measured results.

## Rebuild and submit

```sh
.venv/bin/python build_submission.py
```

This runs the actual organiser submission process, checks its pickle and
source allowlists, plays a clean copy against every dummy, copies matching
sources into `submission/`, and writes a ZIP and SHA-256 manifest.

The exact upload files are:

- `submission/pocketaces.pkl`
- `submission/model.py`
- `submission/poker_eval.py`

The convenience bundle is `submission/pocketaces-submission.zip`. It has
exactly those three basenames at its root. Keep source files and pickle
together; no separate weights or tables are needed.

Open the [Poker Bot Submission Form](https://docs.google.com/forms/d/e/1FAIpQLSe1MQUfkZcGnGBpcgON4J7HumKMBsOekWnr0ZvLcytxA8R5gQ/viewform?usp=dialog).
The current form asks for **Team Name**, **Team Member's Names**, the leader's
**Email**, and a **GitHub repository link**. Enter `PocketAces`, your actual
members/email and `https://github.com/Advaith-Ganesh/Pocket-Aces`. Check the
linked submission directory, then submit the form yourself. If file-upload
fields are added, upload the three individual files above. The assistant
has not submitted the form.

The working deadline supplied in this session is **18:00 Europe/London on
7 November 2026**. The inspected official repository does not publish a
deadline; check organiser announcements if it has changed.

## Competition contract and limitations

The current arena allows **10 seconds per callback**. The bot budgets
sampling to 0.65 seconds, with a fast validated check/fold fallback and
inspectable fallback counters/reasons. It uses no network, files, API calls,
external executable or runtime training during play. Required preflop tables
are built in `__init__`; attributes remain serialisable, including the
organiser-allowlisted `random.Random`. Teams, not seats, key learned data.
`seed` resets hand state, `run` returns one legal action, and `end_game`
consumes remaining events once.

Defaults are 500-chip stacks, 10/20 blinds and duplicate heads-up matches
ranked by bb/100. Raises name integer street totals within `raise_range`;
`call` also checks and handles short all-ins. `legal_actions` is a property.
`pot` already includes current bets; `effective_stack` excludes them. Only
the public view below is used. Board reveals come from the dealer; shown
player cards do not become board cards. Evaluators only receive 5–7 cards.

Ranges, equity realisation and multiway side-pot valuation are heuristic.
Finite samples leave uncertainty near decision thresholds. Dummy-bot wins
and confidence intervals do not predict a tournament win. There is no claim
that this is a solved or optimal strategy.

## Public interface reference

The following upstream table is retained so the official documentation tests
continue to check the exact public contract. Full engine instructions and
organiser tooling remain in [docs/ENGINE_README.md](docs/ENGINE_README.md).

### `GameStateView` (`game_state.py`)

Every name your bot can read; any other raises `AttributeError`. Lists come
back as tuples, indexed by player id.

| The table | |
|---|---|
| `button`, `small_blind`, `big_blind` | player id; chips; chips |
| `stacks`, `bets`, `folded`, `acted` | per player: chips behind, chips bet this street, bools |
| `teams` | per player: team name. Your team is `teams[self.player_id]`; a team's seat is `teams.index(name)` |
| `board` | Cards dealt so far |
| `street` | `"preflop"`, `"flop"`, `"turn"`, `"river"` |
| `pot` | every chip put in this hand, this street's bets included |
| `last_raise` | size of the last full raise this street |
| `to_act` | player id to act, `None` when the street is closed |
| `num_players`, `players_in_hand`, `active_players` | count; ids not folded; ids not folded and not all-in |
| `is_street_closed`, `is_hand_over` | bools |
| `current_bet` | the street total everyone must reach |

| Any player (methods) | |
|---|---|
| `status(player_id)` | `"active"`, `"folded"` or `"all_in"` |
| `effective_stack(player_id)` | their chips behind, capped by the biggest other stack still in (chips already bet excluded) |
| `spr(player_id)` | `effective_stack / pot` |

| Your turn (inside `run`; not meaningful in `end_game`) | |
|---|---|
| `call_amount` | chips a call adds (0 = check) |
| `min_raise_to`, `max_raise_to`, `raise_range` | legal raise totals; `raise_range` is `None` when you cannot raise |
| `can_raise` | bool |
| `legal_actions` | property, no `()`: e.g. `("fold", "call", "raise")` |
| `pot_odds` | `call_amount / (pot + call_amount)`, `0.0` when checking |
| `validate_action(action)` | raises `InvalidAction` if `action` is illegal |


### Cards

`Card.value` is 2–14. The official `evaluate(cards)` accepts 5–7 cards and
returns comparable tuples, higher wins. Never evaluate a two-card preflop
hand. `poker_eval.py` implements the same ordering for simulations and is
checked against the reference evaluator.

### Compare versions

`compare_versions.py` compares trusted pickles using identical decks and
opponent seeds and reports paired per-deck change intervals:

```sh
.venv/bin/python compare_versions.py old/pocketaces.pkl new/pocketaces.pkl --opponents fold tight --seeds 200 201 --deals 400 --out comparison.json
```

Keep each version's matching Python sources next to its pickle, in separate
folders. Use development seeds to choose a candidate and disjoint held-out
seeds to validate it. Avoid treating a confidence interval crossing zero as
evidence of an improvement.
