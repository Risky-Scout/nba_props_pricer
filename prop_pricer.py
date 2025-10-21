
"""
prop_pricer.py — Rebound prop pricer with auditable math.
Populate data/prop_calculator.csv and run. Outputs results/priced_props.csv
"""

import math, csv, json
import pandas as pd

def nb_pmf(x, mu, k):
    if mu <= 0 or k <= 0:
        return 0.0
    p = k / (k + mu)
    from math import lgamma
    return math.exp(lgamma(x + k) - lgamma(k) - lgamma(x + 1) + k*math.log(p) + x*math.log(1 - p))

def nb_cdf(x, mu, k):
    return sum(nb_pmf(i, mu, k) for i in range(0, x+1))

def american_odds_from_prob(p):
    if p <= 0 or p >= 1: return None
    return -round(100 * p/(1-p)) if p >= 0.5 else round(100 * (1-p)/p)

def apply_symmetric_margin(p, hold=0.025):
    q = 1 - p
    p_v = p * (1 + hold/2)
    q_v = q * (1 + hold/2)
    return p_v / (p_v + q_v)

def expected_rebounds_rpg(rpg, mpg, minutes, team_pace, opp_pace, league_pace,
                          team_fg_pct, opp_fg_pct_allowed, league_fg_pct,
                          team_ftr, opp_ftr, league_ftr,
                          gamma_reb_ft=0.0, lineup_factor=1.0, f_pace_exponent=1.0):
    pace_game = 0.5 * (team_pace + opp_pace)
    f_pace = (pace_game / league_pace) ** f_pace_exponent

    miss_team = 1 - team_fg_pct
    miss_opp  = 1 - opp_fg_pct_allowed
    miss_league = 1 - league_fg_pct
    f_miss = ((miss_team + miss_opp)/2) / miss_league * (1 + gamma_reb_ft * (((team_ftr + opp_ftr)/2) - league_ftr))

    rate_per_min = (rpg / mpg) * f_pace * f_miss * lineup_factor
    mu = rate_per_min * minutes
    return mu, f_pace, f_miss, pace_game

def price_row(row):
    # Parse lines
    lines = [float(x) for x in str(row['lines_to_price']).split(';') if str(x).strip()!='']
    mu, f_pace, f_miss, pace_game = expected_rebounds_rpg(
        rpg=float(row['rpg']), mpg=float(row['mpg']), minutes=float(row['minutes_mid']),
        team_pace=float(row['team_pace']), opp_pace=float(row['opp_pace']), league_pace=float(row['league_pace']),
        team_fg_pct=float(row['team_fg_pct']), opp_fg_pct_allowed=float(row['opp_fg_pct_allowed']), league_fg_pct=float(row['league_fg_pct']),
        team_ftr=float(row['team_ftr']), opp_ftr=float(row['opp_ftr']), league_ftr=float(row['league_ftr']),
        gamma_reb_ft=float(row['gamma_reb_ft']), lineup_factor=float(row['lineup_factor'])
    )
    k = float(row['k_dispersion'])
    hold = float(row['hold_margin'])

    out = []
    for L in lines:
        p_over = 1 - nb_cdf(int(L), mu, k)
        p_under = 1 - p_over
        p_over_m = apply_symmetric_margin(p_over, hold)
        p_under_m = 1 - p_over_m
        out.append({
            "player": row['player'],
            "team": row['team'],
            "opponent": row['opponent'],
            "mu": round(mu, 4),
            "k_dispersion": k,
            "line": L,
            "p_over_fair": round(p_over, 4),
            "odds_over_fair": american_odds_from_prob(p_over),
            "p_under_fair": round(p_under, 4),
            "odds_under_fair": american_odds_from_prob(p_under),
            "p_over_market": round(p_over_m, 4),
            "odds_over_market": american_odds_from_prob(p_over_m),
            "p_under_market": round(p_under_m, 4),
            "odds_under_market": american_odds_from_prob(p_under_m),
            "f_pace": round(f_pace, 4),
            "f_miss": round(f_miss, 4),
            "pace_game": round(pace_game, 2),
            "minutes_mid": row['minutes_mid'],
            "lineup_factor": row['lineup_factor'],
            "gamma_reb_ft": row['gamma_reb_ft']
        })
    return out

def main():
    df = pd.read_csv("data/prop_calculator.csv")
    rows = []
    for _, r in df.iterrows():
        rows.extend(price_row(r))
    out_df = pd.DataFrame(rows)
    os.makedirs("results", exist_ok=True)
    out_df.to_csv("results/priced_props.csv", index=False)
    print("Wrote results/priced_props.csv")

if __name__ == "__main__":
    import os
    main()
