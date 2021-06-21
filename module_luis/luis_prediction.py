# This script queries a public LUIS app for IoT using the Python
# LUIS SDK.
#
# This script requires the Cognitive Services LUIS Python module:
#     python -m pip install azure-cognitiveservices-language-luis
#
# This script runs under Python 3.4 or later.


from config import DefaultConfig
CONFIG = DefaultConfig()
import json
from azure.cognitiveservices.language.luis.runtime import LUISRuntimeClient
from msrest.authentication import CognitiveServicesCredentials

# </Dependencies>

# <AuthorizationVariables>
runtime_key = CONFIG.prediction_key
print("runtime_key: {}".format(runtime_key))

runtime_endpoint = CONFIG.prediction_endpoint
print("runtime_endpoint: {}".format(runtime_endpoint))
# </AuthorizationVariables>

# <Client>
# Instantiate a LUIS runtime client
clientRuntime = LUISRuntimeClient(runtime_endpoint, CognitiveServicesCredentials(runtime_key))
# </Client>


# <predict>
def predict(app_id, slot_name):

	request = { "query" : "book a flight from paris to berlin for 2020 between 21th september and 2nd october" }

	# Note be sure to specify, using the slot_name parameter, whether your application is in staging or production.
	response = clientRuntime.prediction.get_slot_prediction(app_id=app_id, slot_name=slot_name, prediction_request=request)

	print("Top intent: {}".format(response.prediction.top_intent))
	print("Sentiment: {}".format (response.prediction.sentiment))
	print("Intents: ")

	for intent in response.prediction.intents:
		print("\t{}".format (json.dumps (intent)))
	print("Entities: {}".format (response.prediction.entities))
# </predict>
