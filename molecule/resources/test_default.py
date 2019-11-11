import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_pkgis_installed(host):
    assert host.package('dnf-automatic').is_installed


def test_config_file(host):
    config_file = host.file('/etc/dnf/automatic.conf')
    assert config_file.is_file
    assert config_file.user == 'root'
    assert config_file.group == 'root'
    assert oct(config_file.mode) == '0o644'


def test_systemd_timer(host):
    systemd_timer = host.service('dnf-automatic.timer')
    assert systemd_timer.is_running
    assert systemd_timer.is_enabled
    # Test actually running dnf-automatic
    assert host.run("dnf-automatic /etc/dnf/automatic.conf").succeeded
