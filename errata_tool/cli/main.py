import sys
import importlib
import errata_tool


USAGE = """
errata-tool [--staging] <command>

Sub Commands:
    erratum    Get an Erratum (advisory)
    product    Get an ET product
    release    Get or create an ET release

Options:
    --staging  Use staging ET instance
"""


def main(argv=None):
    if argv is None:
        argv = sys.argv
    argv.pop(0)  # binary name, "errata-tool"
    if not argv or argv[0] == '--help' or argv[0] == '-h':
        print(USAGE)
        sys.exit(0)
    if argv[0] == '--version':
        print(errata_tool.__version__)
        sys.exit(0)
    if argv[0] == '--staging':
        from errata_tool import ErrataConnector
        ErrataConnector._url = 'https://errata.stage.engineering.redhat.com'
        argv.pop(0)
    if not argv:
        print('missing subcommand')
        print(USAGE)
        sys.exit(1)
    # Dispatch the rest to the subcommand library
    subcommand = argv.pop(0)
    cmdlib = 'errata_tool.cli.%s' % subcommand
    lib = importlib.import_module(cmdlib)
    lib.main(argv)
