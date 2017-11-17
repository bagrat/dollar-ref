from dollar_ref import pluck


def test_pluck():
    root = {
        'not': 'needed',
        'something': 'we need',
        'child': {
            'grandchild': {
                'well': 'I am',
                'pretty': 'much tired',
                'of': 'comming up',
                'with': 'key names',
                'phew': {
                    '$ref': '#/something'
                }
            }
        }
    }

    plucked = pluck(root, 'child', 'grandchild')

    assert plucked == {
        'well': 'I am',
        'pretty': 'much tired',
        'of': 'comming up',
        'with': 'key names',
        'phew': 'we need'
    }
