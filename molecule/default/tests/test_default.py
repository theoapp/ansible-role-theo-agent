import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_theo_binary_file(host):
    f = host.file('/usr/sbin/theo-agent')
    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'


def test_theo_config_file(host):
    f = host.file('/etc/theo-agent/config.yml')
    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'
    conf = f.content
    '''
    url: https://theo.example.com
    token: \
        zdOPNza4jjtceH5F2rU0iOkIJ2xlV4hGUauKT4cNe8HAp+AMnzYEzSc0EIBGM+MJuqL7gLd6bwIP
    cachedir: /var/cache/theo-agent
    verify: False
    '''
    expected = [
        b'url: https://theo.example.com',
        b'token: zdOPNza4jjtceH5F2rU0iOkIJ2xlV4hGUauKT4cNe8HAp'
        b'+AMnzYEzSc0EIBGM+MJuqL7gLd6bwIP',
        b'cachedir: /var/cache/theo-agent',
        b'verify: False'
    ]
    for line in expected:
        assert line in conf
