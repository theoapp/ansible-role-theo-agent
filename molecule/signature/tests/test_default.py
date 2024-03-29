import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_theo_binary_file(host):
    f = host.file('/usr/sbin/theo-agent')
    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'
    assert f.mode == 0o0755


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
    verify: True
    public_key: /etc/theo-agent/public.pem
    hostname-prefix: test-
    '''
    expected = [
        b'url: https://theo.example.com',
        b'token: zdOPNza4jjtceH5F2rU0iOkIJ2xlV4hGUauKT4cNe8HAp'
        b'+AMnzYEzSc0EIBGM+MJuqL7gLd6bwIP',
        b'cachedir: /var/cache/theo-agent',
        b'verify: True',
        b'public_key: /etc/theo-agent/public.pem',
        b'hostname-prefix: test-'
    ]
    for line in expected:
        assert line in conf


def test_theo_public_key_file(host):
    f = host.file('/etc/theo-agent/public.pem')
    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'
