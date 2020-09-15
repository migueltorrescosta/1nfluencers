def get_pruned_subtree(indicators, tree):
    """
    Filters a passed tree to only contain the passed indicators.
    If a theme / subtheme / category has no valid indicators, that entity is removed from the tree.

    Args:  
        indicators: The indicators the client is interested in observing
        tree: The data obtained from python-exerc
    """

    for theme in tree:
        for sub_theme in theme["sub_themes"]:
            for category in sub_theme["categories"]:
                # Removes non-wanted indicators
                category["indicators"] = [indicator for indicator in category["indicators"] if indicator["name"] in indicators]
            # Remove categories without any wanted indicators
            sub_theme["categories"] = [category for category in sub_theme["categories"] if category["indicators"]]
        # Remove sub_themes without any wanted categories / indicators
        theme["sub_themes"] = [sub_theme for sub_theme in theme["sub_themes"] if sub_theme["categories"]]
    # Remove themes without any wanted sub_themes / indicators
    tree = [theme for theme in tree if theme["sub_themes"]]

    return tree


def get_subtree_by_id(ids, tree):
    """
    Filters a passed tree to contain the given ids only.
    If an id is matched, the entire subtree is passed

    Args:  
        ids: The ids we are looking for. They must be of format int
        tree: The data obtained from python-exerc
    """
    def get_wanted_indicators(category):        

        # If the category has a wanted id we return it. Otherwise we return only the wanted IDs of the son indicators.
        # If no indicators are wanted we return an empty list of indicators, but we still return the category.

        if category["id"] not in ids:
            category["indicators"] = [indicator for indicator in category["indicators"] if indicator["id"] in ids]

        return category

    def get_wanted_categories(sub_theme):


        # If the sub theme is in the ids, we return it completely, otherwise we only return the categories wanted / with an wanted indicator
        if sub_theme["id"] not in ids:
            # Removes unwanted categories
            sub_theme["categories"] = list(map(get_wanted_indicators, sub_theme["categories"]))
            sub_theme["categories"] = [category for category in sub_theme["categories"] if category["indicators"] != []]
        return sub_theme

    def get_wanted_sub_themes(theme):


        # If the theme is in the ids, we return it completely, otherwise we only return the sub_themes wanted
        if theme["id"] not in ids:
            # Removes unwanted sub_themes
            theme["sub_themes"] = list(map(get_wanted_categories, theme["sub_themes"]))
            theme["sub_themes"] = [sub_theme for sub_theme in theme["sub_themes"] if sub_theme["categories"] != []]
        return theme


    tree = [get_wanted_sub_themes(theme) for theme in tree]
    tree = [theme for theme in tree if theme["sub_themes"] != []] 


    return tree