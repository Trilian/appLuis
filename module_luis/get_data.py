
import pandas as pd
from . import bot_creation as bc

def load_data(data_path) -> list:
    bot_conversation_df = pd.read_json(data_path)
    turns_series = bot_conversation_df['turns']
    turns_list = turns_series.to_list()

    return turns_list


def key_value_correspondence(association_value) :
    list_key = ['or_city', 'dst_city', 'str_date', 'end_date', 'budget']
    if 'key' in association_value and 'val' in association_value:
        if association_value['key'] in list_key and association_value['val'] != "-1" and association_value['val'] != None:
            cle_value_tuple = (
                association_value['key'], association_value['val'])
            return cle_value_tuple
    return None


def transform_data(data_list):
    # pour toutes les conversations
    list_final = []
    for conversation in data_list:
        # et pour tous les dialogues
        for dialog in conversation:
            if (dialog['author'] == 'user'):
                # le text du dialogue
                text = dialog['text']
                parametres_list = dialog['labels']['acts']
                tuple_list = []
                for parametre in parametres_list:
                    if parametre['args']:
                        for arg in parametre['args']:
                            if not(arg['key'] == 'ref'):
                                cle_value_tuple = key_value_correspondence(arg)
                                if cle_value_tuple:
                                    tuple_list.append(cle_value_tuple)
                            else:
                                annotations_list = arg['val'][0]['annotations']
                                if annotations_list:
                                    for annotation_value in annotations_list:
                                        cle_value_tuple = key_value_correspondence(
                                            annotation_value)
                                        if cle_value_tuple:
                                            tuple_list.append(cle_value_tuple)
                if tuple_list:
                    utterance_tuple = tuple(tuple_list)
                    list_final.append(bc.create_utterance(
                        "BookFlight", text, *utterance_tuple))
    return list_final
