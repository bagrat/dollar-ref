import json

from dollar_ref import resolve


def test_basic(tmpdir):
    root_dir = tmpdir.mkdir('root_dir')
    root_doc = root_dir.join('root.json')

    file_data = {
        'some': 'in_file_data'
    }

    root_doc.write(json.dumps(file_data))

    data = {
        'inline': 'data',
        'file_ref': {
            '$ref': f"{str(root_doc)}#/some"
        }
    }

    resolved = resolve(data)

    assert resolved == {
        'inline': 'data',
        'file_ref': 'in_file_data'
    }


def test_yaml(tmpdir):
    root_dir = tmpdir.mkdir('root_dir')
    root_doc = root_dir.join('root.yaml')

    root_doc.write('''---
        hello: yaml
        thing:
            '$ref': '#/hello'
    ''')

    data = {
        'inline': 'data',
        'file_ref': {
            '$ref': f"{str(root_doc)}#/thing"
        }
    }

    resolved = resolve(data)

    assert resolved == {
        'inline': 'data',
        'file_ref': 'yaml'
    }


def test_not_dict(tmpdir):
    root_dir = tmpdir.mkdir('root_dir')
    root_doc = root_dir.join('root.json')

    file_data = 'some stuff here'

    root_doc.write(json.dumps(file_data))

    data = {
        'inline': 'data',
        'file_ref': {
            '$ref': f"{str(root_doc)}"
        }
    }

    resolved = resolve(data)

    assert resolved == {
        'inline': 'data',
        'file_ref': 'some stuff here'
    }


def test_cwd(tmpdir):
    root_dir = tmpdir.mkdir('root_dir')
    root_doc = root_dir.join('root.json')

    file_data = {
        'some': 'stuff'
    }

    root_doc.write(json.dumps(file_data))

    data = {
        'inline': 'data',
        'file_ref': {
            '$ref': 'root.json#/some'
        }
    }

    resolved = resolve(data, cwd=str(root_dir))

    assert resolved == {
        'inline': 'data',
        'file_ref': 'stuff'
    }


def test_nested(tmpdir):
    root_dir = tmpdir.mkdir('root_dir')

    root_doc = root_dir.join('root.json')
    root_data = {
        'some': 'stuff',
        'some_ref': {
            '$ref': 'child_dir/child.json#/some_key/child_key'
        }
    }
    root_doc.write(json.dumps(root_data))

    child_doc = root_dir.mkdir('child_dir').join('child.json')
    child_data = {
        'some': 'useless thing',
        'now': 'useful data',
        'some_key': {
            'another': 'useless thing',
            'child_key': {
                '$ref': '#/now'
            }
        }
    }
    child_doc.write(json.dumps(child_data))

    data = {
        'file_ref': {
            '$ref': f'{str(root_doc)}#/some_ref'
        }
    }

    resolved = resolve(data)

    assert resolved == {
        'file_ref': 'useful data'
    }


def test_complicated(tmpdir):
    root_dir = tmpdir.mkdir('root_dir')

    root_doc = root_dir.join('root_doc.json')
    root_data = {
        'this': ['is', 'useless'],
        'some_key': {
            'actual': 'stuff',
            'things': [1, {'$ref': 'child1_dir/child1_doc.json#/for_root'}, 3]
        }
    }
    root_doc.write(json.dumps(root_data))

    child1_doc = root_dir.mkdir('child1_dir').join('child1_doc.json')
    child1_data = {
        'again': 'useless',
        'for_root': {
            'childish': 'things',
            'weird': {
                '$ref': '../child2_dir/child2_doc.json#/for_child1'
            }
        }
    }
    child1_doc.write(json.dumps(child1_data))

    child2_doc = root_dir.mkdir('child2_dir').join('child2_doc.json')
    child2_data = {
        'still': 'useless',
        'for_child1': {
            'grand': 'child?',
        }
    }
    child2_doc.write(json.dumps(child2_data))

    data = {
        'some': 'data',
        'file': {
            '$ref': f'{str(root_doc)}#/some_key'
        }
    }

    resolved = resolve(data)

    assert resolved == {
        'some': 'data',
        'file': {
            'actual': 'stuff',
            'things': [
                1,
                {
                    'childish': 'things',
                    'weird': {
                        'grand': 'child?'
                    }
                },
                3
            ]
        }
    }
