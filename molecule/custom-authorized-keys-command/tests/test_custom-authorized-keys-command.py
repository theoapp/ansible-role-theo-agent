"""Role testing files using testinfra."""


def test_sshd_config(host):
    expected = [
        b'AuthorizedKeysCommand /custom/theo/agent/executable --with-custom-args',
    ]
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
