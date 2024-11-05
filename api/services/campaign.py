def is_valid_level(campaign, player):
    campaign_levels = campaign["matchers"]["level"]
    return campaign_levels["min"] <= player["level"] <= campaign_levels["max"]

def has_attr(campaign, player):
    for key, values in campaign["matchers"]["has"].items():
        # Check inventory
        if key == "items":
            for value in values:
                if value not in player["inventory"] or player["inventory"][value] <= 0:
                    return False
        # Check other keys (country, language, gender)
        elif player[key] not in values:
            return False
    return True

def does_not_have_attr(campaign, player):
    for key, values in campaign["matchers"]["does_not_have"].items():
        # Check inventory
        if key == "items":
            for value in values:
                if value in player["inventory"] and player["inventory"][value] > 0:
                    return False
        # Check other keys (country, language, gender)
        elif player[key] in values:
            return False
    return True

def is_valid_campaign(campaign, player):
    for condition in (is_valid_level, has_attr, does_not_have_attr):
        if not condition(campaign, player):
            return False
    return True
