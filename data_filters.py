import functools
import pprint
pp = pprint.PrettyPrinter()

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
    def get_wanted_sub_items(item, tree_structure):

        if tree_structure == []:
            # The tree structure must always start above the last node.
            return "Invalid tree_structure"

        child_items_name = tree_structure[0]
        child_items = item[child_items_name]

        if item["id"] in ids:
            # If the item is in the ids we automatically return all of it
            return item

        if len(tree_structure) == 1:
            # Handles the last node in the structure tree
            item[child_items_name] = [child_item for child_item in child_items if child_item["id"] in ids]

        else:
            # We only keep an item if it has a wanted sub item
            wanted_sub_items_function = functools.partial(get_wanted_sub_items, tree_structure=tree_structure[1:])    
            item[child_items_name] = list(map(wanted_sub_items_function, child_items))
            item[child_items_name] = [child_item for child_item in child_items if child_item[tree_structure[1]] != []]
            
        return item          

    tree_structure = ["sub_themes", "categories", "indicators"]
    tree = [get_wanted_sub_items(theme, tree_structure) for theme in tree]
    tree = [theme for theme in tree if theme["sub_themes"] != []] 

    return tree