#!/bin/bash
PATH=$PATH # existing path goes here
source /opt/anaconda3/bin/activate appointment
python ~/PycharmProjects/passport_appointment/main.py
source /opt/anaconda3/bin/deactivate
