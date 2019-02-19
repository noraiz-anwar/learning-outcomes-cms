import csv
import logging

from learning_outcomes.models import Topic, TopicStructure
from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    """
    help = 'Populates the topic structure'

    def add_arguments(self, parser):
        parser.add_argument(
            '-f', '--file_name',
            default="input.csv",
            help='CSV filename from which to read the topics'
        )

    def handle(self, *args, **options):
        """
        Handler for the command

        It creates topic structure for the given topics in csv file
        """
        csv_filename = options['file_name']

        with open(csv_filename) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            next(csv_reader)  # Skip first line it contain headings

            parent = {}
            for row in csv_reader:
                column = 0
                for topic in row:
                    if topic and column == 0:
                        parent[column] = None
                    if topic:
                        try:
                            topic_metadata = Topic.objects.get_or_create(name=unicode(topic))
                            topic_structure = TopicStructure.objects.create(topic=topic_metadata[0], parent=parent[column])
                            parent[column + 1] = topic_structure
                        except UnicodeDecodeError:
                            pass
                    column += 1
