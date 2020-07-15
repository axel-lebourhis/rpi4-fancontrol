#!/bin/sh -e

DIR=$(pwd)

apt-get install -y python-systemd python3-systemd
ln -sf ${DIR}/fancontrol.py /usr/bin/fancontrol.py
cp ${DIR}/fancontrol.service /lib/systemd/system/.
systemctl daemon-reload
systemctl enable fancontrol.service
systemctl start fancontrol.service
