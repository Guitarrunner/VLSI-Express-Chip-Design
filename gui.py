import vagrant
from fabric.api import *

@task
def mytask():
    run('echo $USER')

v = vagrant.Vagrant()
v.up()
env.hosts = [v.user_hostname_port()]
env.key_filename = v.keyfile()
execute(mytask)