import sys
from errata_tool.product import Product

USAGE = """
errata-tool product <command>

Sub Commands:
    get       Get a product
"""


def get(argv):
    if not argv:
        print('errata-tool product get <name>')
        print('specify a product name, eg. "RHCEPH"')
        sys.exit(1)
    name = argv.pop(0)
    p = Product(name=name)
    print('Name: %s' % p.name)
    print('Description: %s' % p.description)
    print('Supports PDC: %s' % p.supports_pdc)
    print('URL: %s' % p.url)


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
