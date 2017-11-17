import os
import json

import yaml


def resolve(data, root=None, cwd=None):
    if not isinstance(data, dict):
        if isinstance(data, list):
            for i, item in enumerate(data):
                data[i] = resolve(item, root, cwd)

        return data

    if root is None:
        root = data

    if '$ref' not in data:
        for subkey in data:
            data[subkey] = resolve(data[subkey], root, cwd)

        return data

    ref = data['$ref']

    if ref.startswith('#'):
        return resolve_internal(ref, root)
    elif ref.startswith('http://') or ref.startswith('https://'):
        pass  # Not Implemented
    else:
        return resolve_file(ref, cwd)


def _follow_path(ref: str, data: dict):
    if ref in ('', '#', '#/'):
        return data

    ref_path = ref[2:].split('/')

    ref_data = data
    for path_item in ref_path:
        ref_data = ref_data[path_item]

    return ref_data


def resolve_internal(ref: str, root: dict):
    ref_data = _follow_path(ref, root)

    return resolve(ref_data, root=root)


def resolve_file(ref: str, cwd: str):
    ref_split = ref.split('#')

    if len(ref_split) == 1:
        path, in_ref = ref_split[0], ''
    elif len(ref_split) == 2:
        path, in_ref = ref_split
    else:
        pass  # notify error

    in_ref = f"#{in_ref}"

    if not os.path.isabs(path):
        path = os.path.join(cwd, path)

    file_data = read_file(path)

    data = _follow_path(in_ref, file_data)

    new_cwd = os.path.dirname(path)

    return resolve(data, root=file_data, cwd=new_cwd)


def read_file(path):
    with open(path, 'r') as file:
        raw = file.read()

        if raw.startswith('---'):
            data = yaml.load(raw)
        else:
            data = json.loads(raw)

    return data
