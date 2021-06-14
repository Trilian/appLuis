# This script builds a LUIS app, entities, and intents using the Python
# LUIS SDK. Allow to train and publish luis version
#
# This script requires the Cognitive Services LUIS Python module.
# The package is in the file requirements.txt
#
# This script runs under Python 3.4 or later.

# import packages
import time
import json
from azure.cognitiveservices.language.luis.authoring import LUISAuthoringClient
from msrest.authentication import CognitiveServicesCredentials
from ..config import DefaultConfig
CONFIG = DefaultConfig()

# Instantiate a LUIS client
client = LUISAuthoringClient(
    CONFIG.authoring_endpoint, CognitiveServicesCredentials(CONFIG.authoring_key))


def create_app():
    '''
        Creation of Luis application
            Parameters:
                    None
            Returns:
                    app_id,  (string): luis application id
                    app_version (integer): initial version of application
    '''
    app_name = "Fly Bot"
    app_desc = "Flight booking app built with LUIS Python SDK."
    app_version = "0.1"
    app_locale = "en-us"

    app_id = client.apps.add(dict(name=app_name,
                                  initial_version_id=app_version,
                                  description=app_desc,
                                  culture=app_locale))

    print("Created LUIS app {}\n    with ID {}".format(app_name, app_id))
    return app_id, app_version


def add_entities(app_id, app_version):
    '''
        Creation of entities :
            - dst_city
            - or_city
            - budget
            - str_date
            - end_date

            Parameters:
                    app_id : luis application id
                    app_version : initial version of application
            Returns:
                    None
    '''
    dst_city_entity_id = client.model.add_entity(
        app_id, app_version, name="dst_city")
    print("destinationEntityId {} added.".format(dst_city_entity_id))

    or_city_entity_id = client.model.add_entity(
        app_id, app_version, name="or_city")
    print("classEntityId {} added.".format(or_city_entity_id))

    budget_entity_id = client.model.add_entity(
        app_id, app_version, name="budget")
    print("flightEntityId {} added.".format(budget_entity_id))

    start_date_entity_id = client.model.add_entity(
        app_id, app_version, name="str_date")
    print("flightEntityId {} added.".format(start_date_entity_id))

    end_date_entity_id = client.model.add_entity(
        app_id, app_version, name="end_date")
    print("flightEntityId {} added.".format(end_date_entity_id))


def add_intents(app_id, app_version):
    '''
        Creation of intention :
            - BookFlight
            - Cancel
            - Greeting
            - Help
            - Closing

            Parameters:
                    app_id : luis application id
                    app_version : initial version of application
            Returns:
                    None
    '''
    intent_id = client.model.add_intent(app_id, app_version, "BookFlight")
    print("Intent BookFlight {} added.".format(intent_id))

    intent_id = client.model.add_intent(app_id, app_version, "Cancel")
    print("Intent Cancel {} added.".format(intent_id))

    intent_id = client.model.add_intent(app_id, app_version, "Greeting")
    print("Intent Greeting {} added.".format(intent_id))

    intent_id = client.model.add_intent(app_id, app_version, "Help")
    print("Intent Help {} added.".format(intent_id))

    intent_id = client.model.add_intent(app_id, app_version, "Closing")
    print("Intent Closing {} added.".format(intent_id))


def _create_utterance(intent, utterance, *labels):
    '''
        Internal method to format an utterance for luis application
    '''
    text = utterance.lower()

    def label(name, value):
        value = value.lower()
        start = text.index(value)
        return dict(entity_name=name, start_char_index=start,
                    end_char_index=start + len(value))

    return dict(text=text, intent_name=intent,
                entity_labels=[label(n, v) for (n, v) in labels])


def add_utterances(app_id, app_version, data):
    '''
        Creation utterances from a dataset given in parameters

            Parameters:
                    app_id : luis application id
                    app_version : initial version of application
                    data : dataset given the examples to train luis
                           application(intention bookflight)
            Returns:
                    None
    '''
    # Now define the utterances
    utterances = data

    # Add the utterances in batch. You may add any number of example utterances (100 max.)
    # for any number of intents in one call.
    client.examples.batch(app_id, app_version, utterances)

def train_app(app_id, app_version):
    '''
        Train the luis application

            Parameters:
                    app_id : luis application id
                    app_version : initial version of application
            Returns:
                    None
    '''
    client.train.train_version(app_id, app_version)
    waiting = True
    while waiting:
        info = client.train.get_status(app_id, app_version)

        # get_status returns a list of training statuses,
        # one for each model. Loop through them and make sure all are done.
        waiting = any(map(lambda x: x.details.status ==
                      'Queued' or x.details.status == 'InProgress', info))
        if waiting:
            print("Waiting 10 seconds for training to complete...")
            time.sleep(10)

        else:
            print("trained")
            waiting = False


def evaluate_app(list_test, test_path) :
    '''
        Allow to evaluate luis application off line

            Parameters:
                    list_test : list of utterances keep to be evaluated
                    test_path : path to file containing the test data
            Returns:
                    None
    '''
    with open(test_path, "a") as f: 
    
        test_str = json.dumps(list_test)
        test_str = test_str.replace("intent_name","intent")
        test_str = test_str.replace("entity_labels","entities")
        test_str = test_str.replace("entity_name","entity")
        test_str = test_str.replace("start_char_index","startPos")
        test_str = test_str.replace("end_char_index","endPos")

    f.write(test_str)

def publish_app(app_id, app_version):
    '''
        Publish the luis application

            Parameters:
                    app_id : luis application id
                    app_version : initial version of application
            Returns:
                    None
    '''
    client.apps.update_settings(app_id, is_public=True)
    response_endpoint_info = client.apps.publish(
        app_id, app_version, is_staging=False)

    print("Application published. Endpoint URL: " +
          response_endpoint_info.endpoint_url)
