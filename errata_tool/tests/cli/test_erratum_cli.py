import pytest
from errata_tool.cli.erratum import main


class FakeErratum(object):
    def __init__(self, **kwargs):
        pass


def test_no_args():
    with pytest.raises(SystemExit):
        main([''])


def test_help():
    with pytest.raises(SystemExit):
        main(['--help'])


def test_get_no_args():
    with pytest.raises(SystemExit):
        main(['get'])


def test_get(monkeypatch):
    monkeypatch.setattr('errata_tool.cli.erratum.Erratum', FakeErratum)
    main(['get', '12345'])
