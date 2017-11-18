from dollar_ref import resolve


def test_basic():
    data = {
        'some': 'data',
        'other': 'stuff',
        'some_ref': {
            '$ref': '#/other'
        }
    }

    resolved = resolve(data)

    assert resolved == {
        **data,
        'some_ref': 'stuff'
    }


def test_object():
    data = {
        'some': {
            'nested': 'data'
        },
        'other': 'stuff',
        'some_ref': {
            '$ref': '#/some'
        }
    }

    resolved = resolve(data)

    assert resolved == {
        **data,
        'some_ref': {
            'nested': 'data'
        }
    }


def test_nested():
    data = {
        'some': {
            '$ref': '#/other'
        },
        'other': 'stuff',
        'some_ref': {
            '$ref': '#/some'
        }
    }

    resolved = resolve(data)

    assert resolved == {
        **data,
        'some': 'stuff',
        'some_ref': 'stuff'
    }


def test_empty():
    assert {} == resolve({})


def test_non_dict():
    assert resolve(1234) == 1234


def test_list():
    data = {
        'some': 'data',
        'refs': [
            'item',
            {'$ref': '#/some'}
        ]
    }

    resolved = resolve(data)

    assert resolved == {
        'some': 'data',
        'refs': ['item', 'data']
    }


def test_complicated():
    data = {
        'key_1': 1234,
        'key_2': 'abcd',
        'key_3': True,
        'key_4': [1, True, 'three', {'$ref': '#/key_1'}],
        'key_5': {
            'key_5_1': 1234,
            'key_5_2': {
                'key_5_2_1': 'one two three'
            },
            'key_5_3': [123, {'$ref': '#/key_5/key_5_1'}]
        },
        'key_6': {
            'key_6_1': 4567,
            'key_6_2': {
                'key_6_2_1': 'four five six'
            },
            'key_6_3': [456, {'$ref': '#/key_5/key_5_3'}]
        }
    }

    resolved = resolve(data)

    assert resolved == {
        'key_1': 1234,
        'key_2': 'abcd',
        'key_3': True,
        'key_4': [1, True, 'three', 1234],
        'key_5': {
            'key_5_1': 1234,
            'key_5_2': {
                'key_5_2_1': 'one two three'
            },
            'key_5_3': [123, 1234]
        },
        'key_6': {
            'key_6_1': 4567,
            'key_6_2': {
                'key_6_2_1': 'four five six'
            },
            'key_6_3': [456, [123, 1234]]
        }
    }


def test_inplace():
    data = {
        'some': 'data',
        'other': 'stuff',
        'some_ref': {
            '$ref': '#/other'
        }
    }

    resolved = resolve(data)

    assert resolved is data
    assert data['some_ref'] == 'stuff'
