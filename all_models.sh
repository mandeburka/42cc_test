#!/bin/sh
python manage.py all_models 2> $(date +"%Y-%m-%d").dat
