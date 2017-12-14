import pytest
from errata_tool.cli import main
from errata_tool.connector import ErrataConnector


class CallRecorder(object):
    def __call__(self, *args):
        self.args = list(*args)


class FakeModule(object):
    def __getattr__(self, name):
        self.method_name = name
        self.recorder = CallRecorder()
        return self.recorder


class FakeImportlib(object):
    def import_module(self, name):
        self.module_name = name
        self.module = FakeModule()
        return self.module


@pytest.fixture
def importlib(monkeypatch):
    importlib = FakeImportlib()
    monkeypatch.setattr(main, 'importlib', importlib)
    return importlib


def test_short_help():
    with pytest.raises(SystemExit):
        main.main(['errata-tool', '-h'])


def test_help():
    with pytest.raises(SystemExit):
        main.main(['errata-tool', '--help'])


def test_prod_connector(importlib):
    main.main(['errata-tool', 'release'])
    expected = 'https://errata.devel.redhat.com'
    assert ErrataConnector._url == expected


def test_staging_connector(importlib):
    main.main(['errata-tool', '--staging', 'release'])
    expected = 'https://errata.stage.engineering.redhat.com'
    assert ErrataConnector._url == expected


def test_dispatch(importlib):
    main.main(['errata-tool', 'release', 'get', 'rhceph-2.4'])
    assert importlib.module_name == 'errata_tool.cli.release'
    assert importlib.module.method_name == 'main'
    assert importlib.module.recorder.args == ['get', 'rhceph-2.4']
