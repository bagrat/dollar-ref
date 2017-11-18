import json
import logging

from pytest import raises

from dollar_ref.console import main


def test_basic(tmpdir):
    root_dir = tmpdir.mkdir('root_dir')

    root_doc = root_dir.join('root.json')
    root_data = {
        'some': 'data',
        'some_ref': {
            '$ref': 'child_doc.json#/for_root'
        }
    }
    root_doc.write(json.dumps(root_data))

    child_doc = root_dir.join('child_doc.json')
    child_data = {
        'for_root': 'ref_data'
    }
    child_doc.write(json.dumps(child_data))

    out_doc = root_dir.join('out.json')

    main([str(root_doc), str(out_doc)])

    out_data = json.loads(out_doc.read())

    assert out_data == {
        'some': 'data',
        'some_ref': 'ref_data'
    }


def teardown_function():
    log = logging.getLogger('dollar-ref')
    log.handlers = []


def test_input_not_found(capsys):
    with raises(SystemExit):
        main(['/does/not/exist', '/does/not/matter'])

    _, err = capsys.readouterr()

    assert err == "Error: Input file '/does/not/exist' was not found.\n"


def test_output_not_found(tmpdir, capsys):
    input_file = tmpdir.join('input_file.json')
    input_file.write('1234')

    with raises(SystemExit):
        main([str(input_file), '/could/not/write'])

    _, err = capsys.readouterr()

    assert err == "Error: Could not write to output file '/could/not/write'.\n"


def test_resolution_error(tmpdir, capsys):
    input_file = tmpdir.join('input_file.json')
    input_file.write(json.dumps({
        'some': 'data',
        'no_ref': {
            '$ref': '/does/not/exist#/and/matter'
        }
    }))
    output_file = tmpdir.join('output_file.json')

    with raises(SystemExit):
        main([str(input_file), str(output_file)])

    _, err = capsys.readouterr()

    assert err == ("Error: Could not resolve '/does/not/exist#/and/matter', "
                   "'/does/not/exist' file not found.\n")
