
from modulesLuis import load_data,key_value_correspondence, transform_data
from modulesLuis import bot_creation as bc

def test_key_value_correspondence() :
    arg = {'val': 'Caprica', 'key': 'or_city'}
    cle_value_tuple = key_value_correspondence(arg)
    assert  cle_value_tuple == ("or_city", "Caprica")


class TestCreateUtterance :
    data_path = "data/frames.json"
    data_list = load_data(data_path)
    
    def test_create_utterance_from_ref(self) :
        dialog_without_annoations = self.data_list[0:1]
        print(dialog_without_annoations)
        list_final = transform_data(dialog_without_annoations)
        print(list_final)
        assert True

    def test_create_utterance_from_annotations(self) :
        dialog_with_annotations = self.data_list[2:3]
        list_final = transform_data(dialog_with_annotations)
        print(list_final)
        list_final_test = [
            {'text': 'hello there i am looking to go on a vacation with my family to gotham city, can you help me?', 
                'intent_name': 'BookFlight', 
                'entity_labels': [{'entity_name': 'dst_city', 'start_char_index': 63, 'end_char_index': 74}]}, 
            {'text': 'yes i do, it is around $2200', 
                'intent_name': 'BookFlight', 
                'entity_labels': [{'entity_name': 'budget', 'start_char_index': 23, 'end_char_index': 28}]}, 
            {'text': 'we are from neverland', 
                'intent_name': 'BookFlight', 
                'entity_labels': [{'entity_name': 'or_city', 'start_char_index': 12, 'end_char_index': 21}]}, 
            {'text': 'we can depart from toronto', 
                'intent_name': 'BookFlight', 
                'entity_labels': [{'entity_name': 'or_city', 'start_char_index': 19, 'end_char_index': 26}]},
            {'text': 'hmm what options would i have out of toronto?', 
                'intent_name': 'BookFlight', 
                'entity_labels': [{'entity_name': 'or_city', 'start_char_index': 37, 'end_char_index': 44}]}]

        assert list_final_test == list_final