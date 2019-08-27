import csv
import logging

from django.core.management.base import BaseCommand
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
            self.generate_tree(levels, csv_reader, parent_topic_structure[0])

    def generate_tree(self, levels, csv_reader, parent_topic_structure):
        """
        Generates a tree of topic structures using a csv file
        """
        parent = {0: parent_topic_structure}
        row_number = 2
        leaf_node, outcome, outcome_dict = None, None, {}
        for row in csv_reader:
            column = 0
            for data in row:
                if data and data != ' ':
                    if column < levels:
                        leaf_node = self._create_topic_structure(data, parent, column)
                    elif column == levels:
                        outcome = self._add_outcome(data, leaf_node)
                        outcome_dict[row_number] = outcome
                    else:
                        self._add_dependencies(data, outcome, outcome_dict)
                column += 1
            row_number += 1

    def _create_topic_structure(self, topic_name, parent, column):
        """
        Creates a single topic structure
        """
        topic_metadata = Topic.objects.get_or_create(name=topic_name)
        topic_structure = TopicStructure.objects.get_or_create(topic=topic_metadata[0],
                                                               parent=parent[column])
        parent[column + 1] = topic_structure[0]

        return topic_metadata[0]

    def _add_outcome(self, outcome_statement, topic):
        """
        Adds outcome to a topic
        """
        outcome = Outcomes.objects.get_or_create(statement=outcome_statement)
        topic.outcomes.add(outcome[0])
        return outcome[0]

    def _add_dependencies(self, dependencies, outcome, outcome_dict):
        """
        Adds outcome dependencies to the outcome
        """
        indexes = dependencies.split(';')
        for index in indexes:
            outcome.prerequisites.add(outcome_dict[int(index)])
