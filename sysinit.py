#!/usr/bin/python2
from subprocess import call
from os.path import exists

'''
mount kernel filesystems
'''

if call(['mountpoint','-q','/proc']): call(['mount','-t','proc','proc','/proc','-o','nosuid,noexec,nodev'])
if call(['mountpoint','-q','/sys']): call(['mount','-t','sysfs','sys','/sys','-o','nosuid,noexec,nodev'])
if call(['mountpoint','-q','/run']): call(['mount','-t','tmpfs','run','/run','-o','mode=0755,nosuid,nodev'])
if call(['mountpoint','-q','/dev']): call(['mount','-t','devtmpfs','dev','/dev','-o','mode=0755,nosuid'])
call(['mkdir','-p','/dev/pts','/dev/shm'])
if call(['mountpoint','-q','/dev/pts']): call(['mount','-t','devpts','devpts','/dev/pts','-o','nosuid,noexec,nodev'])
if call(['mountpoint','-q','/dev/shm']): call(['mount','-t','tmpfs','shm','/dev/shm','-o','nosuid,noexec,nodev'])
if call('findmnt / --options ro &>/dev/null',shell=True): call(['mount','-o','remount,ro','/'])
call(['/sbin/bootlogd','-p','/run/bootlogd.pid'])

'''
set host name
'''
# we would do that but its better to do it kernel level

'''
do hwclock
'''
# always use utc for now
call(['hwclock','--systz','--utc','--noadjfile'])

'''
do udevd modprobe
'''
call(['/usr/lib/systemd/systemd-udevd','--daemon'])
call(['udevadm','trigger','--action=add','--type=subsystems'])
call(['udevadm','trigger','--action=add','--type=devices'])
call(['udavadm','settle'])

'''
do ... something... having to do with the voncsole
'''
call(['/usr/lib/systemd/systemd-vconsole-setup'])

'''
bring up loopback
'''
call(['ip','link','set','up','dev','lo'])

'''
setup encrypted partitions
'''
# read the /etc/crypttab into a list
f=open('/etc/crypttab')
lines=[]
for line in f.readlines:
    if line[0] == '#': continue
    tmp=line.split(' ')
    i=0
    while i<len(tmp):
        if tmp[i] == '':
            tmp.pop(i)
        else:
            i+=1
        lines.append(tmp)
f.close()

print("starting test shell")
call(['/bin/bash'])
