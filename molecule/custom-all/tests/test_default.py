import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_theo_binary_file(host):
    f = host.file('/usr/local/bin/theo')
    assert f.exists
    assert f.is_file
    assert f.user == 'root'
    assert f.group == 'root'
    print("{} vs {}".format(f.mode, oct(f.mode)))
    assert oct(f.mode) == '0o755'


def test_theo_cache_dir(host):
    f = host.file('/var/cache/theo')
    assert f.exists
    assert f.is_directory
    assert f.user == 'theo'
    assert f.group == 'root'


def test_theo_config_file(host):
    f = host.file('/var/lib/theo/theo.yml')
    assert f.exists
    assert f.is_file
    assert f.user == 'root'
    assert f.group == 'root'
    conf = f.content
    '''
    url: https://theo.example.com
    token: \
        zdOPNza4jjtceH5F2rU0iOkIJ2xlV4hGUauKT4cNe8HAp+AMnzYEzSc0EIBGM+MJuqL7gLd6bwIP
    cachedir: /var/cache/theo
    verify: True
    public_key: /var/lib/theo/public.pem
    '''
    expected = [
        b'url: https://theo.example.com',
        b'token: zdOPNza4jjtceH5F2rU0iOkIJ2xlV4hGUauKT4cNe8HAp'
        b'+AMnzYEzSc0EIBGM+MJuqL7gLd6bwIP',
        b'cachedir: /var/cache/theo',
        b'verify: True',
        b'public_key: /var/lib/theo/public.pem'
    ]
    for line in expected:
        assert line in conf


def test_theo_public_key_file(host):
    f = host.file('/var/lib/theo/public.pem')
    assert f.exists
    assert f.is_file
    assert f.user == 'root'
    assert f.group == 'root'


def test_sshd_config(host):
    distro = os.environ['MOLECULE_DISTRO']
    if distro == 'debian8':
        expected = get_sshd_config_pre_v69()
    elif distro == 'ubuntu1404':
        expected = get_sshd_config_pre_v69()
    else:
        expected = get_sshd_config_v69()
    f = host.file('/etc/ssh/sshd_config')
    config = f.content
    configlines = []
    for line in config.splitlines():
        if not line.startswith(b'#'):
            configlines.append(line)
    '''
        I don't want to use something like:
            assert set(expected).issubset(configlines)
        Because there's no detail of the missing line(s)
    '''
    errors = []
    for line in expected:
        if line not in configlines:
            errors.append(line)

    if len(errors):
        print('Failed test_sshd_config, missing line(s)')
        for error in errors:
            print(error)
        assert False


def get_sshd_config_pre_v69():
    return [
        b'AuthorizedKeysCommandUser theo',
        b'AuthorizedKeysCommand /usr/local/bin/theo '
        b'-config-file /var/lib/theo/theo.yml %u',
        b'AuthorizedKeysFile /var/cache/theo/%u'
    ]


def get_sshd_config_v69():
    return [
        b'AuthorizedKeysCommandUser theo',
        b'AuthorizedKeysCommand /usr/local/bin/theo '
        b'-config-file /var/lib/theo/theo.yml -fingerprint %f %u',
        b'AuthorizedKeysFile /var/cache/theo/%u'
    ]
