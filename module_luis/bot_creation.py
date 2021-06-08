# Microsoft Azure Language Understanding (LUIS) - Build App
#
# This script builds a LUIS app, entities, and intents using the Python
# LUIS SDK.  A separate sample trains and publishes the app.
#
# This script requires the Cognitive Services LUIS Python module:
#     python -m pip install azure-cognitiveservices-language-luis
#
# This script runs under Python 3.4 or later.

from azure.cognitiveservices.language.luis.authoring import LUISAuthoringClient
from msrest.authentication import CognitiveServicesCredentials

import datetime
import json
import os
import time
from ..config import DefaultConfig
CONFIG = DefaultConfig()

# Instantiate a LUIS client
client = LUISAuthoringClient(
    CONFIG.authoring_endpoint, CognitiveServicesCredentials(CONFIG.authoring_key))

def create_app():
    '''
        Création de l'application Luis
            Parameters:
                    None
            Returns:
                    app_id,  (string): l'id de l'application
                    app_version (integer): la version initiale de l'application
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


# </createApp>

# Declare entities:
#
#   Destination - A simple entity that will hold the flight destination
#
#   Class - A hierarchical entity that will hold the flight class
#           (First, Business, or Economy)
#
#   Flight - A composite entity represeting the flight (including
#               class and destination)
#
# Creating an entity (or other LUIS object) returns its ID.
# We don't use IDs further in this script, so we don't keep the return value.
# <addEntities>
    """[summary]
    """


def add_entities(app_id, app_version):
    dstCityEntityId = client.model.add_entity(
        app_id, app_version, name="dst_city")
    print("destinationEntityId {} added.".format(dstCityEntityId))

    orCityEntityId = client.model.add_entity(
        app_id, app_version, name="or_city")
    print("classEntityId {} added.".format(orCityEntityId))

    budgetEntityId = client.model.add_entity(
        app_id, app_version, name="budget")
    print("flightEntityId {} added.".format(budgetEntityId))

    strDateEntityId = client.model.add_entity(
        app_id, app_version, name="str_date")
    print("flightEntityId {} added.".format(strDateEntityId))

    endDateEntityId = client.model.add_entity(
        app_id, app_version, name="end_date")
    print("flightEntityId {} added.".format(endDateEntityId))


# </addEntities>

# Declare an intent, FindFlights, that recognizes a user's Flight request
# Creating an intent returns its ID, which we don't need, so don't keep.
# <addIntents>
def add_intents(app_id, app_version):
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
# </addIntents>


# Helper function for creating the utterance data structure.
# <createUtterance>
def create_utterance(intent, utterance, *labels):
    """Add an example LUIS utterance from utterance text and a list of
	   labels.  Each label is a 2-tuple containing a label name and the
	   text within the utterance that represents that label.
	   Utterances apply to a specific intent, which must be specified."""

    text = utterance.lower()

    def label(name, value):
        value = value.lower()
        start = text.index(value)
        return dict(entity_name=name, start_char_index=start,
                    end_char_index=start + len(value))

    return dict(text=text, intent_name=intent,
                entity_labels=[label(n, v) for (n, v) in labels])


# </createUtterance>

# Add example utterances for the intent.  Each utterance includes labels
# that identify the entities within each utterance by index.  LUIS learns
# how to find entities within user utterances from the provided examples.
#
# Example utterance: "find flights in economy to Madrid"
# Labels: Flight -> "economy to Madrid" (composite of Destination and Class)
#         Destination -> "Madrid"
#         Class -> "economy"
# <addUtterances>
def add_utterances_flight(app_id, app_version, data):
    # Now define the utterances
    utterances = data

    # Add the utterances in batch. You may add any number of example utterances
    # for any number of intents in one call.
    client.examples.batch(app_id, app_version, utterances)
    print("{} example utterance(s) added.".format(len(utterances)))
# </addUtterances>


# </createUtterance>

# Add example utterances for the intent.  Each utterance includes labels
# that identify the entities within each utterance by index.  LUIS learns
# how to find entities within user utterances from the provided examples.
#
# Example utterance: "find flights in economy to Madrid"
# Labels: Flight -> "economy to Madrid" (composite of Destination and Class)
#         Destination -> "Madrid"
#         Class -> "economy"
# <addUtterances>
def add_utterances_default(app_id, app_version):
    # Now define the utterances
    utterances = [
        create_utterance("Cancel","abort"),
        create_utterance("Cancel","cancel"),
        create_utterance("Cancel","disregard"),
        create_utterance("Cancel","do not do it"),
        create_utterance("Cancel","do not do that"),
        create_utterance("Cancel","don't"),
        create_utterance("Cancel","don't do it"),
        create_utterance("Cancel","don't do that"),

        create_utterance("Greeting","good afternoon"),
        create_utterance("Greeting","good evening"),
        create_utterance("Greeting","good morning"),
        create_utterance("Greeting","good night"),
        create_utterance("Greeting","hello"),
        create_utterance("Greeting","hello bot"),
        create_utterance("Greeting","hi"),
        create_utterance("Greeting","hi bot"),
        create_utterance("Greeting","hiya"),
        create_utterance("Greeting","how are you"),
        create_utterance("Greeting","how are you doing today?"),
        create_utterance("Greeting","how are you doing?"),
        create_utterance("Greeting","how are you today?"),

        create_utterance("Help","help"),
        create_utterance("Help","help me"),
        create_utterance("Help","help me please"),
        create_utterance("Help","help please"),
        create_utterance("Help","i am stuck"),
        create_utterance("Help","i'm stuck"),
        create_utterance("Help","help please"),
        create_utterance("Help","what can i say"),
        create_utterance("Help","what can you do"),
        create_utterance("Help","what can you help me with"),
        create_utterance("Help","what do i do now?"),
        create_utterance("Help","what do i do?"),
        create_utterance("Help","why doesn't this work ?"),
        create_utterance("Help","please help me"),

        create_utterance("Cancel","i would like to cancel"),
        create_utterance("Cancel","never mind"),
        create_utterance("Cancel","please cancel"),
        create_utterance("Cancel","please disregard"),
        create_utterance("Cancel","please stop"),
        create_utterance("Cancel","stop"),

        create_utterance("Closing","Good Bye"),
        create_utterance("Closing","See you again"),
        create_utterance("Closing","See you later"),
        create_utterance("Closing","Tchao"),
    ]

    # Add the utterances in batch. You may add any number of example utterances
    # for any number of intents in one call.
    client.examples.batch(app_id, app_version, utterances)
    print("{} example utterance(s) added.".format(len(utterances)))
# </addUtterances>


# <train>
def train_app(app_id, app_version):
    client.train.train_version(app_id, app_version)
    waiting = True
    while waiting:
        info = client.train.get_status(app_id, app_version)

        # get_status returns a list of training statuses, one for each model. Loop through them and make sure all are done.
        waiting = any(map(lambda x: 'Queued' ==
                      x.details.status or 'InProgress' == x.details.status, info))
        if waiting:
            print("Waiting 10 seconds for training to complete...")
            time.sleep(10)

        else: 
            print ("trained")
            waiting = False
# </train>

# <publish>
def publish_app(app_id, app_version):
    client.apps.update_settings(app_id, is_public=True)
    responseEndpointInfo = client.apps.publish(
        app_id, app_version, is_staging=False)
    print("Application published. Endpoint URL: " +
          responseEndpointInfo.endpoint_url)

# </publish>
