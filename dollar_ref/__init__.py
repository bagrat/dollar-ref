

def resolve_local(data, root=None):
    if not isinstance(data, dict):
        if isinstance(data, list):
            for i, item in enumerate(data):
                data[i] = resolve_local(item, root)

        return data

    if root is None:
        root = data

    if '$ref' not in data:
        for subkey in data:
            data[subkey] = resolve_local(data[subkey], root)

        return data

    ref = data['$ref']
    ref_path = ref[2:].split('/')

    ref_data = root
    for path_item in ref_path:
        ref_data = ref_data[path_item]
    
    return ref_data
