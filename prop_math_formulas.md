# Prop Model Math (Rebounds)

This document captures the exact mathematics used in the rebound prop pricer and the **real inputs** we populated for the Lakers @ Warriors opener.

## 1) Expected rebounds (RPG route)

For a player with rebounds-per-game `RPG` and minutes-per-game `MPG`, baseline per-minute rate is `RPG/MPG`. We then adjust for game context:

- Pace factor:  
  `f_pace = ((pace_team + pace_opp)/2) / pace_league`

- Miss factor (field-goal driven, with FT term optional via `gamma`):  
  `f_miss = (((1 - FG%_team) + (1 - FG%_allowed_opp))/2) / (1 - FG%_league) * (1 + gamma * (((FTr_team + FTr_opp)/2) - FTr_league))`

- Lineup factor: multiplicative uplift/downgrade if role/news suggests change in rebound share.

The expected rebounds at a target minutes `M` is:  
`μ = (RPG/MPG) * f_pace * f_miss * lineup_factor * M`

**Numbers used (sourced)**

- Lakers team (2024-25): pace **97.58**, FG% **0.479**, FT% **0.785**, FGA **85.5**, FTA **23.2** ⇒ `FTr = 23.2/85.5 = 0.2716`. cite: StatMuse LAL team page 2024-25
- Warriors opponent allowed (2024-25): Opp FG% **0.456**, Opp FT% **0.767**, Opp FTA **22.4**, Opp FGA **90.4** ⇒ `Opp FTr ≈ 0.248`. pace **98.67**. cite: StatMuse GSW team page 2024-25
- League baselines (editable constants in code): pace **98.5**, FG% **0.475**, FT% **0.785**, FTr **0.26**.

We set `gamma = 0` so FT rebound tweaks are off (you can enable later).

### Austin Reaves
- RPG **4.5**, MPG **34.9**, target minutes **35**, lineup factor **1.0**
- `pace_game = (97.58 + 98.67)/2 = 98.12`  
- `f_pace = pace_game / 98.5 = 0.9962`  
- `miss_team = 1 - 0.479 = 0.521`  
- `miss_opp = 1 - 0.456 = 0.544`  
- `miss_league = 1 - 0.475 = 0.525`  
- `f_miss = ((miss_team + miss_opp)/2) / miss_league = 1.0143`  
- `rate_per_min = (4.5/34.9) * f_pace * f_miss * 1.0`  
- `μ_Reaves = rate_per_min * 35 = 4.560`

### Rui Hachimura
- RPG **5.0**, MPG **31.7**, target minutes **32**, lineup factor **1.05**
- `pace_game = 98.12`  
- `f_pace = 0.9962`  
- `f_miss` as above (same opponent), identical value.  
- `rate_per_min = (5.0/31.7) * f_pace * f_miss * 1.05`  
- `μ_Rui = rate_per_min * 32 = 5.355`

## 2) Distribution for counts

We use a Negative Binomial NB2 with mean `μ` and dispersion `k`.  
`Var[X] = μ + μ²/k`.  
PMF: `P(X=x) = C(x+k-1, x) * (k/(k+μ))^k * (μ/(k+μ))^x`.

Interpretation: smaller `k` ⇒ more overdispersion vs. Poisson. Guards/wings often `k ≈ 6–9`, bigs `≈ 8–12` (tune by backtest).

## 3) Pricing a line L.5

- Over(L.5): `P(X ≥ L+1) = 1 - CDF(L; μ,k)`
- Under(L.5): complement.
- Convert fair `p` to fair American odds: 
  - if `p ≥ 0.5`: `-100*p/(1-p)` else `+100*(1-p)/p`.
- Apply symmetric hold `h` in probability-space, then renormalize:
  - `p_over^mkt = (p_over * (1 + h/2)) / ((p_over * (1 + h/2)) + (p_under * (1 + h/2)))`

We used `h = 0.025` (2.5%).

## 4) Sanity checks you can re-run

- Change minutes to low/high and confirm μ scales linearly.
- Toggle `gamma` from 0 → 0.1 and see FT rebound impact.
- Replace league baselines with your own published averages — see `config` in the script.