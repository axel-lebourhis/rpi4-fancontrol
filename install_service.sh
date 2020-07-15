#!/bin/sh -e

ln -sf ./fancontrol.py /usr/bin/fancontrol.py
cp ./fancontrol.service /lib/systemd/system/.
systemctl daemon-reload
systemctl enable fancontrol.service
systemctl start fancontrol.service
