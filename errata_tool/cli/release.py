import argparse
import sys
from errata_tool.release import Release
from errata_tool.release import NoReleaseFoundError

USAGE = """
errata-tool release <command>

Sub Commands:
    get       Get a release
    create    Create a new release
"""


def get(argv):
    if not argv:
        print('errata-tool release get <name>')
        print('specify a release name, eg. "rhceph-3.0"')
        sys.exit(1)
    name = argv.pop(0)
    try:
        r = Release(name=name)
        print('Name: %s' % r.name)
        print('Description: %s' % r.description)
        print('URL: %s' % r.url)
    except NoReleaseFoundError:
        print('%s release not found' % name)
        sys.exit(1)


def create(argv):
    # There are many arguments to create(), and they might change over time.
    # Use named args here for future flexibility.
    parser = argparse.ArgumentParser(prog='errata-tool release create')
    req = parser.add_argument_group('required named arguments')
    req.add_argument('--name', required=True, help='eg. "rhceph-2.4"')
    req.add_argument('--product', required=True, help='eg. "RHCEPH"')
    req.add_argument('--type', required=True, help='eg. "QuarterlyUpdate"')
    req.add_argument('--program_manager', required=True, help='eg. "anharris"')
    req.add_argument('--blocker_flags', required=True, help='eg. "ceph-2.y"')
    args = parser.parse_args(argv)
    try:
        r = Release(name=args.name)
        print('%s is already defined at %s' % (r.name, r.url))
        sys.exit(1)
    except NoReleaseFoundError:
        pass
    r = Release.create(
        name=args.name,
        product=args.product,
        type=args.type,
        program_manager=args.program_manager,
        blocker_flags=args.blocker_flags,
    )
    print('created new %s release' % args.name)
    print('visit %s to add PDC associations' % r.edit_url)


def main(argv):
    if not argv or argv[0] == '--help' or argv[0] == '-h':
        print(USAGE)
        sys.exit(0)
    command = argv.pop(0)
    if command == 'get':
        get(argv)
    elif command == 'create':
        create(argv)
    else:
        print('unknown command %s' % command)
        print(USAGE)
        sys.exit(1)
