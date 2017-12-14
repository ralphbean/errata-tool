import pytest
from errata_tool.cli.release import main
from errata_tool.release import NoReleaseFoundError


class FakeRelease(object):
    def __init__(self, **kwargs):
        self.name = kwargs['name']
        self.description = 'Foo description'
        self.url = 'https://errata.devel.redhat.com/myrelease'
        self.edit_url = 'https://errata.devel.redhat.com/myrelease/edit'


class FakeMissingRelease(object):
    def __init__(self, **kwargs):
        raise NoReleaseFoundError

    @classmethod
    def create(cls, **kwargs):
        name = kwargs['name']
        return FakeRelease(name=name)


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
    monkeypatch.setattr('errata_tool.cli.release.Release', FakeRelease)
    main(['get', 'rhceph-3.0'])


def test_get_missing(monkeypatch):
    monkeypatch.setattr('errata_tool.cli.release.Release', FakeMissingRelease)
    with pytest.raises(SystemExit):
        main(['get', 'missing-3.0'])


def test_create_no_args():
    with pytest.raises(SystemExit):
        main(['create'])


def test_create(monkeypatch):
    monkeypatch.setattr('errata_tool.cli.release.Release', FakeMissingRelease)
    main(['create',
          '--name', 'rhceph-2.4',
          '--product', 'RHCEPH',
          '--type', 'QuarterlyUpdate',
          '--program_manager', 'anharris',
          '--blocker_flags', 'ceph-2.y'])
