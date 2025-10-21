# Fair vs. Market Probability

**Fair probability** comes from your model of the underlying event with no bookmaker margin.  
**Market probability** embeds the bookmaker's overround (vig/hold).

For a two-way Over/Under:
- Start with fair `p_over` and `p_under = 1 - p_over`.
- Apply a symmetric hold `h` in probability space and renormalize:
  `p_over^mkt = (p_over * (1 + h/2)) / (p_over * (1 + h/2) + p_under * (1 + h/2))`.

Convert resulting probabilities to American odds in the UI for readability. The code exposes both.