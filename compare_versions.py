"""Compare two trusted submission pickles on identical duplicate deals.

Use separate folders containing each version's pickle and Python sources.
Example: python compare_versions.py old/pocketaces.pkl new/pocketaces.pkl
         --opponents fold tight --seeds 200 201 --deals 400 --out result.json
Results include paired per-deck change intervals, not just point estimates.
"""

import argparse
import json
from pathlib import Path

from arena.match import MatchConfig, play_match
from arena.players import player
from evals.score import score
from evals.stats import ci95, mean_and_se


def deal_values(log):
    hero = log.names[0]
    values = [0.0] * log.config.deals
    for hand in log.hands:
        seat = hand.seats.index(hero)
        values[hand.deal] += hand.net[seat] / (2 * log.config.big_blind)
    return values


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('baseline')
    parser.add_argument('candidate')
    parser.add_argument('--opponents', nargs='+',
                        default=['fold', 'call', 'random', 'shove', 'tight', 'equity'])
    parser.add_argument('--seeds', nargs='+', type=int, default=[200, 201])
    parser.add_argument('--deals', type=int, default=400)
    parser.add_argument('--out', type=Path)
    args = parser.parse_args()
    rows = []
    for opponent in args.opponents:
        logs = [[], []]
        deltas = []
        for seed in args.seeds:
            for version, path in enumerate([args.baseline, args.candidate]):
                logs[version].append(play_match(
                    [player(path), player(opponent)],
                    MatchConfig(deals=args.deals, seed=seed)))
            a, b = (deal_values(group[-1]) for group in logs)
            deltas.extend(y - x for x, y in zip(a, b))
        a, b = map(score, logs)
        mean, se = mean_and_se(deltas)
        row = dict(opponent=opponent, seeds=args.seeds, deals_per_seed=args.deals,
                   hands_per_version=a.hands,
                   baseline_bb100=a.bb_per_100[0], baseline_ci95=a.ci95[0],
                   candidate_bb100=b.bb_per_100[0], candidate_ci95=b.ci95[0],
                   paired_delta_bb100=100 * mean,
                   paired_delta_ci95=100 * ci95(se, len(deltas)),
                   baseline_faults=a.faults[0], candidate_faults=b.faults[0],
                   max_seconds=max(a.max_move_seconds[0], b.max_move_seconds[0]))
        rows.append(row)
        print(json.dumps(row), flush=True)
        if args.out:
            args.out.write_text(json.dumps(rows, indent=2) + '\n', encoding='utf-8')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
