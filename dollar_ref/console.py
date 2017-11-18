import argparse
import os
import json
import sys
import logging

import yaml
from termcolor import colored

from dollar_ref import resolve, read_file, ResolutionError


VERBOSITY = {
    0: logging.INFO,
    1: logging.DEBUG
}


class DrefLogFormatter(logging.Formatter):
    colors = {
        logging.ERROR: 'red',
        logging.DEBUG: 'blue',
        logging.INFO: 'white'
    }
    prefixes = {
        logging.ERROR: 'Error: '
    }

    def __init__(self, use_color=True):
        super().__init__()

        self.use_color = use_color

    def format(self, record):
        prefix = self.prefixes.get(record.levelno, '')

        return self.color_message(f'{prefix}{record.msg}',
                                  record.levelno)

    def color_message(self, msg, levelno):
        if not self.use_color:
            return msg

        color = self.colors.get(levelno, 'white')

        return colored(msg, color)


class DrefLogFilter(logging.Filter):
    def __init__(self, *levels):
        super().__init__()

        self.levels = levels

    def filter(self, record):
        if record.levelno in self.levels:
            return 1

        return 0


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('input_uri', help='')
    parser.add_argument('output_file', help='')
    parser.add_argument("-v", "--verbosity",
                        action="count", default=0,
                        help='')

    return parser.parse_args(args)


def main(args=None):
    args = parse_args(sys.argv[1:] if args is None else args)

    log_level = VERBOSITY.get(args.verbosity, logging.INFO)

    out_handler = logging.StreamHandler(sys.stdout)
    out_handler.setFormatter(DrefLogFormatter(use_color=sys.stdout.isatty()))
    out_handler.addFilter(DrefLogFilter(logging.WARN,
                                        logging.INFO,
                                        logging.DEBUG))

    err_handler = logging.StreamHandler(sys.stderr)
    err_handler.setFormatter(DrefLogFormatter(use_color=sys.stderr.isatty()))
    err_handler.addFilter(DrefLogFilter(logging.ERROR))

    log = logging.getLogger('dollar-ref')
    log.addHandler(out_handler)
    log.addHandler(err_handler)
    log.setLevel(log_level)

    try:
        data = read_file(args.input_uri)
        cwd = os.path.dirname(args.input_uri)
    except FileNotFoundError:
        log.error(f"Input file '{args.input_uri}' was not found.")
        sys.exit(1)

    try:
        resolved = resolve(data, cwd=cwd,
                           external_only=True)

        with open(args.output_file, 'w') as out:
            if args.output_file.endswith(('yml', 'yaml')):
                raw_out = yaml.dump(resolved,
                                    explicit_start=True,
                                    default_flow_style=False)
            else:
                raw_out = json.dumps(resolved)

            out.write(raw_out)
    except FileNotFoundError:
        log.error(f"Could not write to output file '{args.output_file}'.")
        sys.exit(1)
    except ResolutionError as exc:
        log.error(str(exc))
        sys.exit(1)

    log.info(f"Successfully resolved '{args.input_uri}' "
             f"into '{args.output_file}'.")
