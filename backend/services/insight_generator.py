PROS_TEMPLATES = {
    "High ROE": "Company has delivered strong return on equity, indicating efficient capital utilization.",
    "Moderate ROE": "Company has maintained a healthy return on equity.",
    "Low debt levels": "Company has a strong balance sheet with very low debt.",
    "Manageable debt": "Company has manageable debt levels.",
    "Strong sales growth": "Company has delivered strong sales growth in recent periods.",
    "Moderate sales growth": "Company has shown moderate sales growth."
}

CONS_TEMPLATES = {
    "Low ROE": "Company has a low return on equity, indicating weaker capital efficiency.",
    "High debt burden": "Company carries a high debt burden which may impact profitability.",
    "Declining sales": "Company has experienced a decline in sales growth."
}


def generate_insights(pros_flags: dict, cons_flags: dict, max_items=3):

    # Convert flags into readable sentences
    

    # rank pros higher value 
    ranked_pros = sorted(
        pros_flags.items(),
        key=lambda x: (x[1] is not None, x[1]),
        reverse=True
    )[:max_items]

    pros_text = [
        PROS_TEMPLATES.get(flag)
        for flag, _ in ranked_pros
        if flag in PROS_TEMPLATES
    ]

    # Rank cons lower value
    ranked_cons = sorted(
        cons_flags.items(),
        key=lambda x: (x[1] is not None, x[1])
    )[:max_items]

    cons_text = [
        CONS_TEMPLATES.get(flag)
        for flag, _ in ranked_cons
        if flag in CONS_TEMPLATES
    ]

    

    return pros_text, cons_text
