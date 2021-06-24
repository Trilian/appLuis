#!/usr/bin/env python3

import os

""" Luis Configuration """
class DefaultConfig:

    AUTHORING_KEY = os.environ.get("authoringKey", "")
    AUTHORING_ENDPOINT = os.environ.get("authoringEndpoint", "")
    
    PREDICTION_KEY = os.environ.get("PredictionKey","")
    PREDICTION_ENDPOINT = os.environ.get("predictionEndpoint", "")
