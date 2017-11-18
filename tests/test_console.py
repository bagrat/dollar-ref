import json
import logging
from unittest.mock import patch, Mock

from pytest import raises
from termcolor import colored

from dollar_ref.console import main, DrefLogFormatter


def teardown_function():
    log = logging.getLogger('dollar-ref')
    log.handlers = []


def test_basic(tmpdir, capsys):
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

    stdout, _ = capsys.readouterr()

    assert out_data == {
        'some': 'data',
        'some_ref': 'ref_data'
    }
    assert stdout == (f"Successfully resolved '{str(root_doc)}' "
                      f"into '{str(out_doc)}'.\n")


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


def test_yaml_output(tmpdir):
    input_file = tmpdir.join('input_file.yaml')
    input_file.write(json.dumps({
        'hello': 'yaml'
    }))

    output_file = tmpdir.join('output_file.yml')

    main([str(input_file), str(output_file)])

    assert output_file.read() == '---\nhello: yaml\n'


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
    assert not output_file.isfile()


def test_from_cmd_line(script_runner):
    with patch('sys.argv', []):
        result = script_runner.run('dref',
                                   '/does/not/exist', '/does/not/matter')

        assert result.success is False
        assert result.stderr == ("Error: Input file '/does/not/exist' "
                                 "was not found.\n")


def test_color_fromatter():
    formatter = DrefLogFormatter(use_color=True)

    record = Mock()
    record.levelno = logging.ERROR
    record.msg = 'hello'

    assert formatter.format(record) == colored('Error: hello', 'red')
