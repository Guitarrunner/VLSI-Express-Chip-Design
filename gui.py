import vagrant
from fabric.api import *

@task
def mytask():
    
    run('sudo verible/bazel-bin/verilog/tools/lint/verible-verilog-lint /vagrant_data/utils/sample8.v >log.txt')
    run('ls')

v = vagrant.Vagrant()
v.up()
env.hosts = [v.user_hostname_port()]
env.key_filename = v.keyfile()
env.warn_only = True

execute(mytask)