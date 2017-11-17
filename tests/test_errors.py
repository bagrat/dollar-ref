import json

from pytest import raises

from dollar_ref import (
    resolve,
    InternalResolutionError, FileResolutionError,
    ResolutionError, DecodeError
)


def test_bad_internal_ref():
    data = {
        'real': 'stuff',
        'bad_ref': {
            '$ref': '#/does/not/exist'
        }
    }

    with raises(InternalResolutionError):
        resolve(data)


def test_bad_file_ref():
    data = {
        'real': 'stuff',
        'bad_ref': {
            '$ref': '/not/existing/file#/well/this/does/not/matter'
        }
    }

    with raises(FileResolutionError):
        resolve(data)


def test_bad_json(tmpdir):
    bad_json = tmpdir.join('bad.json')
    bad_json.write('!very #bad ^stuff')

    data = {
        '$ref': f'{str(bad_json)}'
    }

    with raises(DecodeError):
        resolve(data)


def test_bad_yaml(tmpdir):
    bad_yaml = tmpdir.join('bad.json')
    bad_yaml.write('{[!very #bad yaml')

    data = {
        '$ref': f'{str(bad_yaml)}'
    }

    with raises(DecodeError):
        resolve(data)


def bad_ref():
    data = {
        'real': 'stuff',
        'bad_ref': {
            '$ref': '%real$wierd&things'
        }
    }

    with raises(FileResolutionError):
        resolve(data)


def test_web():
    data = {
        'real': 'stuff',
        'bad_ref': {
            '$ref': 'http://example.com#/well/this/does/not/matter'
        }
    }

    with raises(ResolutionError):
        resolve(data)
