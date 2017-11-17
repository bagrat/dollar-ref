from pytest import raises

from dollar_ref import (
    resolve, InternalResolutionError, FileResolutionError, ResolutionError
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


def test_web():
    data = {
        'real': 'stuff',
        'bad_ref': {
            '$ref': 'http://example.com#/well/this/does/not/matter'
        }
    }

    with raises(ResolutionError):
        resolve(data)
