import csv
from django.core.management.base import BaseCommand
from healthbot.models import MedicalCondition

class Command(BaseCommand):
    help = 'Import medical conditions from a CSV file'

    def handle(self, *args, **kwargs):
        # Path to your CSV file
        with open('/Users/momenon/PycharmProjects/DjangoProject1/data/medical-conditions.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                # Assuming the condition name is in the first column
                condition_name = row[0]
                MedicalCondition.objects.get_or_create(name=condition_name)
                self.stdout.write(self.style.SUCCESS(f'Condition "{condition_name}" imported successfully!'))
