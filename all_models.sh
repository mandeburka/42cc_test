#!/bin/sh
python manage.py all_models --settings="mandeburka_test.settings" 2> $(date +"%Y-%m-%d").dat
