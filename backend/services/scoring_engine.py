
def score_company(row):
    # a single company row (Series)
    # Returns score, pros_flags, cons_flags

    score = 50
    pros = {}
    cons = {}

    roe = row.get("roe")
    debt = row.get("debt_to_equity")
    growth = row.get("sales_growth")

    # roe
    if roe is not None:
        if roe >= 15:
            score += 25
            pros["High ROE"] = roe
        elif roe >= 10:
            score += 15
            pros["Moderate ROE"] = roe
        else:
            score -= -15
            cons["Low ROE"] = roe
        
    # debt to equity
    if debt is not None:
        if debt <= 0.5:
            score += 20
            pros["Low debt levels"] = debt
        elif debt <= 1:
            score += 10
            pros["Manageable debt"] = debt
        elif debt > 1.5:
            score -= 20
            cons["High debt burden"] = debt


    # sales growth
    if growth is not None:
        if growth >= 10:
            score += 20
            pros["Strong sales growth"] = growth
        elif growth >= 5:
            score += 10
            pros["Moderate sales growth"] = growth
        elif growth < 0:
            score -= 20
            cons["Declining sales"] = growth


    # normalize score
    score = max(0, min(score, 100))

    return score, pros, cons



