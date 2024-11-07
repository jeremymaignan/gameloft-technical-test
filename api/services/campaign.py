def is_valid_level(matchers, player):
    if "level" not in matchers:
        return True

    campaign_levels = matchers["level"]
    return campaign_levels["min"] <= player["level"] <= campaign_levels["max"]

def has_attr(matchers, player):
    if "has" not in matchers:
        return True

    for key, values in matchers["has"].items():
        # Check inventory
        if key == "items":
            for value in values:
                if value not in player["inventory"] or player["inventory"][value] <= 0:
                    return False
        # Check other keys (country, language, gender)
        elif key not in player or player[key] not in values:
            return False
    return True

def does_not_have_attr(matchers, player):
    if "does_not_have" not in matchers:
        return True

    for key, values in matchers["does_not_have"].items():
        # Check inventory
        if key == "items":
            for value in values:
                if value in player["inventory"] and player["inventory"][value] > 0:
                    return False
        # Check other keys (country, language, gender)
        elif key not in player or player[key] in values:
            return False
    return True

def is_valid_campaign(campaign, player):
    #TODO: Should we use attributes enabled, start_date, end_date?
    if "matchers" not in campaign:
        return True

    for condition in (is_valid_level, has_attr, does_not_have_attr):
        if not condition(campaign["matchers"], player):
            return False
    return True
