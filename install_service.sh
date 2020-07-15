#!/bin/sh -e

ln -s ./fancontrol.py /usr/bin/fancontrol.py
chmod 755 ./fancontrol
cp ./fancontrol /etc/init.d/.
systemctl daemon-reload
update-rc.d fancontrol defaults
/etc/init.d/fancontrol start
