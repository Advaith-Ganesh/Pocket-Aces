# Attribution and provenance

Pocket Aces is our poker bot for the Manchester AI Society / MUDS AI
hackathon. The bot strategy (`model.py`), fast evaluator (`poker_eval.py`),
additional bot tests, packaging helper and Pocket Aces documentation were
written for this project.

The poker engine, card/action/state interfaces, arena, evaluation tools,
submission tool, pinned requirements and original tests come from
[Manchester-AI-Society/poker_bot](https://github.com/Manchester-AI-Society/poker_bot),
revision `b852bd52c48cffe0e203b669a07fb198e36fff8e`.
They are included for local development and organiser-compatible validation.
We do not claim authorship of that infrastructure. Its source notices and
Git history have been retained; engine, arena, evals and official tests are
unmodified. The original README is retained at `docs/ENGINE_README.md`.

The existing bot was transferred from our fork,
`Advaith-Ganesh/poker_bot`, branch `codex/pocketaces-bot`, revision
`44f747b1a251c126a4fd04e976886c289b5a9750`. A complete Git bundle and source
archive were preserved locally before the transfer. Its report and concise
validation output are retained in `docs/BASELINE_REPORT.md` and
`docs/BASELINE_VALIDATION.txt`.

No LICENSE, COPYING or NOTICE file was present in the inspected upstream
revision. No blanket licence is added that would purport to relicense the
upstream engine. Third-party dependencies retain their own licences.
