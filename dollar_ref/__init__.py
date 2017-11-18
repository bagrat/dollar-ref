"""
Main functionality of `dollar-ref` library.
"""
import os
import logging
import json

import yaml


class ResolutionError(Exception):
    """
    General error that happens during resolution.
    """
    pass


class InternalResolutionError(ResolutionError):
    """
    Error while resolving internal referenses.
    """
    pass


class FileResolutionError(ResolutionError):
    """
    Error while resolving a reference to another file.
    """
    pass


class DecodeError(ResolutionError):
    """
    Error while deciding a referenced file.
    """
    pass


log = logging.getLogger('dollar-ref.lib')


def resolve(data, root=None, cwd: str = None,
            *, external_only: bool = False) -> dict:
    """
    Recursively resolve any references in `data` **inplace**.

    If `root` is provided, all internal references are resolved relative
    to that document.

    If `cwd` is provided, all external references are resolved relative
    to that path.

    If `external_only` is passed as `True` then only external references
    are reloved.

    Additionally, returns the resolved document.
    """
    if not isinstance(data, dict):
        if isinstance(data, list):
            for i, item in enumerate(data):
                data[i] = resolve(item, root, cwd,
                                  external_only=external_only)

        return data

    if root is None:
        root = data

    if '$ref' not in data:
        for subkey in data:
            data[subkey] = resolve(data[subkey], root, cwd,
                                   external_only=external_only)

        return data

    ref = data['$ref']

    if ref.startswith('#'):
        if not external_only:
            return resolve_internal(ref, root)

        return data
    elif ref.startswith(('http://', 'https://')):
        raise ResolutionError("Web resolution is not implemented yet")
    else:
        return resolve_file(ref, cwd, external_only=external_only)


def _follow_path(ref: str, data: dict) -> dict:
    """
    Returns the object from `data` at `ref`.

    Example:
        Given:
            data = {
                'key1': {
                    'key2': 'value'
                }
            }
            ref = '#/key1/key2'

        The result will be:
            'value'
    """
    if ref in ('', '#', '#/'):
        return data

    ref_path = ref[2:].split('/')

    ref_data = data
    for path_item in ref_path:
        try:
            ref_data = ref_data[path_item]
        except KeyError:
            raise InternalResolutionError(
                f"Error resolving '{ref}', "
                f"'{path_item}' not found in '{ref_data}'."
            )

    return ref_data


def resolve_internal(ref: str, root: dict) -> dict:
    """
    Resolve an internal reference specified by `ref`.

    The resolution is performed based on the `root` document.
    """
    ref_data = _follow_path(ref, root)

    return resolve(ref_data, root=root)


def resolve_file(ref: str, cwd: str, *, external_only: bool = False) -> dict:
    """
    Resolve an external file reference specified by `ref`.

    This function also recursively resolves the contents of the referenced
    file.

    If the reference is not an absolute path, then is is resolved relative
    to `cwd`.

    If `external_only` is `True`, the internal references of the referenced
    file contents are not resolved and are kept as is.
    """
    ref_split = ref.split('#')

    if len(ref_split) == 1:
        path, in_ref = ref_split[0], ''
    elif len(ref_split) == 2:
        path, in_ref = ref_split

    in_ref = f"#{in_ref}"

    if not os.path.isabs(path):
        path = os.path.join(cwd, path)

    try:
        file_data = read_file(path)
    except FileNotFoundError:
        raise FileResolutionError(
            f"Could not resolve '{ref}', "
            f"'{path}' file not found."
        )

    data = _follow_path(in_ref, file_data)

    new_cwd = os.path.dirname(path)

    return resolve(data, root=file_data, cwd=new_cwd,
                   external_only=external_only)


def read_file(path: str) -> dict:
    """
    Read and decode a file specified by `path`.

    This function automatically detects whether the file is a JSON or YAML
    and decodes accordingly.
    """
    with open(path, 'r') as file:
        raw = file.read()

        try:
            if raw.startswith('---'):
                data = yaml.load(raw)
            else:
                data = json.loads(raw)
        except json.decoder.JSONDecodeError as exc:
            raise DecodeError(
                f"Error decoding '{path}' file."
            ) from exc

    return data


def pluck(root, *path):
    data = root
    for path_item in path:
        data = data[path_item]

    return resolve(data, root)
