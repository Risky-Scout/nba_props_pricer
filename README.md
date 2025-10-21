# NBA Rebound Prop Pricer (LAL @ GSW example)

This folder contains:
- `docs/prop_math_formulas.md`: full math and the **real numbers** used
- `docs/fair_vs_market_prob.md`: how fair probs differ from market probs
- `docs/data_dictionary.md`: what each CSV column means
- `scripts/prop_pricer.py`: single-file runner
- `data/prop_calculator.csv`: **pre-populated rows** for Austin Reaves & Rui Hachimura vs Warriors (no placeholders)

## Sources (copy these in your notes / one-pager)
- Lakers 2024-25 team stats (FG%, FT%, FGA, FTA, FT%, pace): StatMuse team page.  
  https://www.statmuse.com/nba/team/los-angeles-lakers-15/stats/2025
- Warriors 2024-25 team stats + opponent allowed (Opp FG%, Opp FT%, Opp FTA/FGA), pace: StatMuse team page.  
  https://www.statmuse.com/nba/team/golden-state-warriors-6/2025
- Austin Reaves per-game RPG/MPG (2024-25): ESPN player page.  
  https://www.espn.com/nba/player/_/id/4066457/austin-reaves
- Rui Hachimura per-game RPG/MPG (2024-25): ESPN player page.  
  https://www.espn.com/nba/player/_/id/4066648/rui-hachimura

## Run
From this folder:
```
python scripts/prop_pricer.py
```
Result: `results/priced_props.csv` with fair + market probabilities/odds.

## Refreshing data fast
- Update `data/prop_calculator.csv` with:
  - team/opponent pace, FG%, FGA, FTA (to compute FTr), FT% for both teams
  - player RPG/MPG and minutes scenario
- You can keep `gamma_reb_ft=0` to ignore FT rebound contributions (safe), or set to `0.05–0.12` later.
- Edit `league_*` constants in code top or add a config file if you prefer published league averages.