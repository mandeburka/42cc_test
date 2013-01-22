from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from django.db.utils import DatabaseError

class Command(BaseCommand):
    help = 'Print all project models and their quantity in database'

    def handle(self, *args, **options):
        try:
            for model_type in ContentType.objects.all():
                s = '%s_%s - %d\n' % (
                    model_type.app_label,
                    model_type.model,
                    len(model_type.model_class().objects.all()))
                self.stdout.write(s)
                self.stderr.write('Error: %s' % s)
        except DatabaseError:
            pass
