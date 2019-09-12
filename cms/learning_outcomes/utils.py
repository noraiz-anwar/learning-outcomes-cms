from .models import Outcomes, Topic, TopicStructure


def generate_tree(levels, csv_reader, parent_topic_structure):
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
                    leaf_node = _create_topic_structure(data, parent, column)
                elif column == levels:
                    outcome = _add_outcome(data, leaf_node)
                    outcome_dict[row_number] = outcome
                else:
                    _add_dependencies(data, outcome, outcome_dict)
            column += 1
        row_number += 1


def _create_topic_structure(topic_name, parent, column):
    """
    Creates a single topic structure
    """
    topic_metadata = Topic.objects.get_or_create(name=topic_name)
    topic_structure = TopicStructure.objects.get_or_create(topic=topic_metadata[0],
                                                           parent=parent[column])
    parent[column + 1] = topic_structure[0]

    return topic_metadata[0]


def _add_outcome(outcome_statement, topic):
    """
    Adds outcome to a topic
    """
    outcome = Outcomes.objects.get_or_create(statement=outcome_statement)
    topic.outcomes.add(outcome[0])
    return outcome[0]


def _add_dependencies(dependencies, outcome, outcome_dict):
    """
    Adds outcome dependencies to the outcome
    """
    indexes = dependencies.split(';')
    for index in indexes:
        outcome.prerequisites.add(outcome_dict[int(index)])
