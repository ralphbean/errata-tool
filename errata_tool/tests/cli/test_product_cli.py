import pytest
from errata_tool.cli.product import main


class FakeProduct(object):
    def __init__(self, name):
        self.name = name
        self.description = 'Foo description'
        self.url = 'https://errata.devel.redhat.com/myrelease'
        self.supports_pdc = True


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
    monkeypatch.setattr('errata_tool.cli.product.Product', FakeProduct)
    main(['get', 'RHCEPH'])
