from dollar_ref import pluck


root_doc = {
    'we-do-not': 'need-this',
    'sub-document': {
        'target': {
            'awesome': 'data',
            'we': {
                '$ref': '#/we-do-not'
            }
        }
    }
}


target = pluck(root_doc, 'sub-document', 'target')

assert target == {
    'awesome': 'data',
    'we': 'need-this'
}
