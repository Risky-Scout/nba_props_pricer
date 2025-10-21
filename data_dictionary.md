# Data Dictionary (inputs for `data/prop_calculator.csv`)

- player: string, player name
- team, opponent: team abbreviations (e.g., LAL, GSW)
- rpg, mpg: prior season rebounds and minutes (per game)
- minutes_low/mid/high: scenario minutes (integers)
- team_pace, opp_pace, league_pace: possessions per 48
- team_fg_pct: team FG% (0-1). If you only have eFG%, you may use it as a proxy; see docs.
- opp_fg_pct_allowed: opponent defensive FG% allowed (0-1); eFG% proxy acceptable.
- league_fg_pct: league FG% baseline (0-1).
- team_ft_pct, opp_ft_pct_allowed, league_ft_pct: free-throw % (0-1). (Only used if `gamma_reb_ft > 0`.)
- team_ftr, opp_ftr, league_ftr: free-throw rate = FTA/FGA (0-1).
- gamma_reb_ft: weight (0-0.2) for FT miss contribution to rebounds; `0` disables.
- lineup_factor: multiplicative role/news factor, default 1.00.
- k_dispersion: negative binomial dispersion `k` (>0).
- hold_margin: desired symmetric margin (e.g., 0.025 = 2.5%).
- lines_to_price: semicolon-separated lines (e.g., `4.5;5.5;6.5`).
- Optional (for TRB-route, can be blank if not used): `team_trb_pct`, `opp_trb_pct_allowed`, `others_trb_share_sum`, `repl_trb_pct`.