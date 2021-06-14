
import pandas as pd
from . import luis_function as bc


def load_data(data_path) -> list:
    '''
    Load dataset used to train luis application

            Parameters:
                    data_path : path for data json file

            Returns:
                    turns_list : a list of dialog
    '''
    bot_conversation_df = pd.read_json(data_path)
    turns_series = bot_conversation_df['turns']
    turns_list = turns_series.to_list()

    return turns_list


def _key_value_correspondence(association_value):
    '''
    Internal method to find the correspondence between key/value
    '''
    list_key = ['or_city', 'dst_city', 'str_date', 'end_date', 'budget']
    if 'key' in association_value and 'val' in association_value:
        if association_value['key'] in list_key and association_value['val'] != "-1" \
            and association_value['val'] != None:
            cle_value_tuple = (
                association_value['key'], association_value['val'])
            return cle_value_tuple
    return None


def transform_data(data_list):
    '''
    Transform data list of dialogs to get only the value to send to luis Application
     user dialog, remove -1 value...

            Parameters:
                    data_list : a list of dialog
            Returns:
                    list_final : the dialog list cleaned
    '''
    # pour toutes les conversations
    list_final = []
    for conversation in data_list:
        # et pour tous les dialogues
        for dialog in conversation:
            if dialog['author'] == 'user':
                # le text du dialogue
                text = dialog['text']
                parametres_list = dialog['labels']['acts']
                tuple_list = []
                for parametre in parametres_list:
                    if parametre['args']:
                        for arg in parametre['args']:
                            if not arg['key'] == 'ref':
                                cle_value_tuple = _key_value_correspondence(
                                    arg)
                                if cle_value_tuple:
                                    tuple_list.append(cle_value_tuple)
                            else:
                                annotations_list = arg['val'][0]['annotations']
                                if annotations_list:
                                    for annotation_value in annotations_list:
                                        cle_value_tuple = _key_value_correspondence(
                                            annotation_value)
                                        if cle_value_tuple:
                                            tuple_list.append(cle_value_tuple)
                if tuple_list:
                    utterance_tuple = tuple(tuple_list)
                    list_final.append(bc._create_utterance(
                        "BookFlight", text, *utterance_tuple))
    return list_final


def create_data(data_path):
    '''
    Just create utterances for intentions except bookflight

            Parameters:
                    text_list : a list of text
            Returns:
                    list_final : the dialog list cleaned
    '''
    list_final = []
    with open(data_path, "r") as f:
        data_intentions = f.readlines()
        for text_intention in data_intentions:
            list_intention = text_intention.split(",")
            list_final.append(bc._create_utterance(list_intention[0], list_intention[1]))

    return list_final