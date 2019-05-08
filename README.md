Ansible role: Theo Agent
=========

[![Build Status](https://travis-ci.org/theoapp/ansible-role-theo-agent.svg?branch=master)](https://travis-ci.org/theoapp/ansible-role-theo-agent)

An Ansible Role that installs [TheoAgent](https://github.com/theoapp/theo-agent)
on RHEL/CentOS, Debian/Ubuntu.

Requirements
------------

This role assumes SSH server is installed on the target host.

Role Variables
--------------

Required variables:
```
theo_url:
theo_client_token:
```

For variables that can be customised, see `defaults/main.yml`

Dependencies
------------

None.

Example Playbook
----------------

    - hosts: servers
      vars:
        - theo_url: https://theo.example.com
        - theo_client_token: zdOPNza4jjtceH5F2rU0iOkIJ2xlV4hGUauKT4cNe8HAp+AMnzYEzSc0EIBGM+MJuqL7gLd6bwIP
      roles:
         - { role: theoapp/ansible-theo-agent }

License
-------

BSD

Author Information
------------------

This role was create in 2019 by [Gizero](https://github.com/gizero)
