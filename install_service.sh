#!/bin/sh -e

DIR=$(pwd)

ln -sf ${DIR}/fancontrol.py /usr/bin/fancontrol.py
cp ${DIR}/fancontrol.service /lib/systemd/system/.
systemctl daemon-reload
systemctl enable fancontrol.service
systemctl start fancontrol.service
