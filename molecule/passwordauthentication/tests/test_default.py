import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_sshd_config(host):
    distro = os.getenv('MOLECULE_DISTRO', 'centos7')
    if distro == 'centos6':
        expected = get_sshd_config_centos6()
    elif distro == 'debian8':
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

    if(len(errors)):
        print('Failed test_sshd_config, missing line(s)')
        for error in errors:
            print(error)
        assert False


def get_sshd_config_centos6():
    return [
        b'PasswordAuthentication yes',
        b'AuthorizedKeysCommandRunAs theo-agent',
        b'AuthorizedKeysCommand /usr/sbin/theo-agent',
        b'AuthorizedKeysFile /var/cache/theo-agent/%u'
    ]


def get_sshd_config_pre_v69():
    return [
        b'PasswordAuthentication yes',
        b'AuthorizedKeysCommandUser theo-agent',
        b'AuthorizedKeysCommand /usr/sbin/theo-agent',
        b'AuthorizedKeysFile /var/cache/theo-agent/%u'
    ]


def get_sshd_config_v69():
    return [
        b'PasswordAuthentication yes',
        b'AuthorizedKeysCommandUser theo-agent',
        b'AuthorizedKeysCommand /usr/sbin/theo-agent -fingerprint %f %u',
        b'AuthorizedKeysFile /var/cache/theo-agent/%u'
    ]
