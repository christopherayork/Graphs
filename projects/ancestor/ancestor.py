

def earliest_ancestor(ancestors, starting_node, path=None, recursive=False):
    if path is None: path = []
    options = []
    for new_vert in ancestors:
        if new_vert[1] == starting_node:
            new_path = list(path)
            new_path.append(new_vert)
            options = options + earliest_ancestor(ancestors, new_vert[0], new_path, True)
    if not len(options): options.append(path)
    if recursive is True: return options
    else:
        largest = None
        for new_path in options:
            if largest is None: largest = new_path
            elif len(new_path) > len(largest): largest = new_path
        if largest is None or not len(largest): return -1
        return largest[-1][0]
