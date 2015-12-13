#!/usr/bin/env python 
# -*- coding: utf-8 -*-
__author__ = 'duc_tin'

import os, sys
from subprocess import call

addr0, port0 = '', ''
exclude0 = ''


def proxy_on(address, port, no_proxy=''):
    proxy = address+':'+port
    no_proxy= ','.join(["localhost,127.0.0.0/8", no_proxy])

    # apt-get and update-manager
    contents = ['Acquire::{0}::Proxy "{0}://{1}";\n'.format(kind, proxy) for kind in ('http', 'https', 'socks', 'ftp')]
    line = ''.join(contents)[:-1]
    if not os.path.exists('/etc/apt/apt.conf'):
        call('sudo touch /etc/apt/apt.conf'.split())
    with open('/tmp/temp', 'w+') as tmp:
        with open('/etc/apt/apt.conf', 'r') as apt:
            cache = [l for l in apt.readlines() if 'proxy' not in l]
        tmp.writelines(cache)
        tmp.write(line)
    call('sudo mv {} /etc/apt/apt.conf'.format(tmp.name).split())

    # other programs
    contents = ['{0}_proxy="http://{1}/"\n'.format(kind, proxy) for kind in ('http', 'https', 'socks', 'ftp')]
    line = ''.join(contents)+'no_proxy="{}"\n'.format(no_proxy)
    contents = ['{0}_PROXY="http://{1}/"\n'.format(kind, proxy) for kind in ('HTTP', 'HTTPS', 'SOCKS', 'FTP')]
    line += ''.join(contents)+'NO_PROXY="{}"\n'.format(no_proxy)
    with open('/tmp/temp', 'w+') as tmp:
        with open('/etc/environment', 'r') as env:
            cache = [l for l in env.readlines() if 'proxy' not in l.lower()]
        tmp.writelines(cache)
        tmp.write(line)
    call('sudo mv {} /etc/environment'.format(tmp.name).split())

    # GTK3 applications
    call("gsettings set org.gnome.system.proxy mode 'manual'".split())
    call("gsettings set org.gnome.system.proxy.http host '{}'".format(address).split())
    call("gsettings set org.gnome.system.proxy.http port {}".format(port).split())
    call("gsettings set org.gnome.system.proxy.https host '{}'".format(address).split())
    call("gsettings set org.gnome.system.proxy.https port {}".format(port).split())
    call(["gsettings", "set", "org.gnome.system.proxy", "ignore-hosts", '{}'.format(str(no_proxy.split(',')))])


def proxy_off():
    # apt-get and update-manager
    if not os.path.exists('/etc/apt/apt.conf'):
        call('sudo touch /etc/apt/apt.conf'.split())
    with open('/tmp/temp', 'w+') as tmp:
        with open('/etc/apt/apt.conf', 'r') as apt:
            cache = [l for l in apt.readlines() if 'proxy' not in l]
        tmp.writelines(cache)
    call('sudo mv {} /etc/apt/apt.conf'.format(tmp.name).split())

    # other programs
    with open('/tmp/temp', 'w+') as tmp:
        with open('/etc/environment', 'r') as env:
            cache = [l for l in env.readlines() if 'proxy' not in l.lower()]
        tmp.writelines(cache)
    call('sudo mv {} /etc/environment'.format(tmp.name).split())

    # GTK3 applications
    call("gsettings set org.gnome.system.proxy mode 'none'".split())


if __name__ == '__main__':
    help = """ Usage: ./proxy_manager.py cmd [proxy_address port] [no_proxy_address]
    where:
    cmd                'on' or 'off',  turn on or off proxy
    proxy_address       addess of the proxy, not include 'http://' and similar
    port                port of the proxy
    no_proxy_address    address to be exclude from proxy

Example:
    You have a proxy 'http://myproxy.com:8080'
    Set system wide proxy:
        $ ./proxy_manager.py on myproxy.com 8080

    You don't want to use this proxy on .mydomain.com, www.abc.com:
        $ ./proxy_manager.py on myproxy.com 8080 .mydomain.com www.abc.com

    You don't need proxy anymore:
        $ ./proxy_manager.py off

Set default proxy:
    $ gedit proxy_manager.py

    Then replace these below lines
        addr0, port0 = '', ''
        exclude0 = ''
    into:
        addr0, port0 = 'myproxy.com', '8080'
        exclude0 = '.mydomain.com,www.abc.com'

    $ ./proxy_manager.py on
"""
    args = sys.argv[1:]
    if not args:
        print(help)

    else:
        cmd = args[0]
        if cmd == 'on':
            addr, port = args[1:2], args[2:3]
            if not all([addr, port]):
                if all([addr0, port0]):
                    addr, port = addr0, port0
                else:
                    print('Error: Please specify proxy address and port')
                    sys.exit(1)

            exclude = ','.join(args[3:])+exclude0
            proxy_on(addr, port, exclude)
        elif cmd == 'off':
            proxy_off()
        else:
            print(help)