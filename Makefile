MANAGE=django-admin.py

test:
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=mandeburka_test.settings $(MANAGE) test contact

run:
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=mandeburka_test.settings $(MANAGE) runserver

syncdb:
    PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=mandeburka_test.settings $(MANAGE) syncdb --noinput
