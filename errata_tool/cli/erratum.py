import sys
from errata_tool.erratum import Erratum

USAGE = """
errata-tool erratum <command>

Sub Commands:
    get       Get an erratum (advisory)
"""


def get(argv):
    if not argv:
        print('errata-tool erratum get <id>')
        print('specify an advisory ID, eg. "12345"')
        sys.exit(1)
    errata_id = argv.pop(0)
    e = Erratum(errata_id=errata_id)
    print(e)


def main(argv):
    if not argv or argv[0] == '--help' or argv[0] == '-h':
        print(USAGE)
        sys.exit(0)
    command = argv.pop(0)
    if command == 'get':
        get(argv)
    else:
        print('unknown command %s' % command)
        print(USAGE)
        sys.exit(1)
