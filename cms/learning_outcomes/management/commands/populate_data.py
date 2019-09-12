import csv
import logging

from django.core.management.base import BaseCommand
from learning_outcomes.utils import generate_tree
from learning_outcomes.models import Outcomes, Topic, TopicStructure

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Populates the topic structure'

    def add_arguments(self, parser):
        parser.add_argument(
            '-f', '--file_name',
            default="input.csv",
            help='CSV filename from which to read the topics'
        )
        parser.add_argument(
            '-p', '--parent',
            default="parent topic",
            help='Name of parent of topic structure'
        )

    def handle(self, *args, **options):
        """
        Handler for the command

        It creates topic structure for the given topics in csv file
        and adds outcomes to the leaf node
        """
        csv_filename = options['file_name']
        parent_name = options['parent']
        levels = 0

        with open(csv_filename) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            headings = next(csv_reader)

            # Determine the topic hierarchy levels
            for heading in headings:
                if heading.lower() in ["topic", "topics"]:
                    levels += 1

            parent_topic = Topic.objects.get_or_create(name=parent_name)
            parent_topic_structure = TopicStructure.objects.get_or_create(topic=parent_topic[0],
                                                                          parent=None)
            generate_tree(levels, csv_reader, parent_topic_structure[0])
