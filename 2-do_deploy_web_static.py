#!/usr/bin/python3
"""Deploy web static to different servers"""
import re
from fabric.context_managers import cd
from fabric.api import env, put, run, sudo
from os.path import join, exists, splitext


env.user = "ubuntu"
env.hosts = ["98.80.123.16", "3.80.121.113"]
env.key_filename = '~/.ssh/id_rsa'

def do_deploy(archive_path):
    if not os.path.exists(archive_path):
        print("Archive file doesn't exist")
        return False

    archive_filename = os.path.basename(archive_path)
    archive_filename_without_extension = os.path.splitext(archive_filename)[0]

    local_file_path = '/alu-AirBnB_clone_v2/web_static/0-index.html'
    if not os.path.exists(local_file_path):
        print("Local file doesn't exist")
        return False

    with Connection(host=env.hosts[0]) as c:
        c.put(archive_path, '/tmp/' + archive_filename)
        c.run('mkdir -p /data/web_static/releases/' + archive_filename_without_extension + '/')
        c.run('tar -xzf /tmp/' + archive_filename + ' -C /data/web_static/releases/' + archive_filename_without_extension + '/')
        c.run('rm /tmp/' + archive_filename)
        c.put(local_file_path, '/data/web_static/releases/' + archive_filename_without_extension + '/hbnb_static/0-index.html')
        c.run('rm -rf /data/web_static/current')
        c.run('ln -s /data/web_static/releases/' + archive_filename_without_extension + '/ /data/web_static/current')

    with Connection(host=env.hosts[1]) as c:
        c.put(archive_path, '/tmp/' + archive_filename)
        c.run('mkdir -p /data/web_static/releases/' + archive_filename_without_extension + '/')
        c.run('tar -xzf /tmp/' + archive_filename + ' -C /data/web_static/releases/' + archive_filename_without_extension + '/')
        c.run('rm /tmp/' + archive_filename)
        c.put(local_file_path, '/data/web_static/releases/' + archive_filename_without_extension + '/hbnb_static/0-index.html')
        c.run('rm -rf /data/web_static/current')
        c.run('ln -s /data/web_static/releases/' + archive_filename_without_extension + '/ /data/web_static/current')

    print("New version deployed!")
    return True
