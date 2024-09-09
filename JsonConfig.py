import json
import os
import sys


def get_json_config(file_path):

    if getattr(sys, 'frozen', False):
        # Jika aplikasi sudah di-compile menjadi .exe
        application_path = os.path.dirname(sys.executable)
    else:
        # Jika berjalan dalam mode skrip Python biasa
        application_path = os.path.dirname(os.path.abspath(__file__))
    
    config_path = os.path.join(application_path, file_path)

    with open(config_path, 'r') as file:
        data = json.load(file)
    return data
