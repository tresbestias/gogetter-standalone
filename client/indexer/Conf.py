
import json
import socket
import os
CONFIG_FOLDER = os.path.dirname(os.path.realpath(__file__)) +'/settings'
class Configuration():

    CLINET_ID = None

    #CONFIG_FOLDER = './settings'
    CONFIG_FILE = CONFIG_FOLDER+'/settings.json'
    INDEXED_FOLDERS = ['/home/shibin/Documents/test']
    LOCAL_IP = None
    # get the already stored client id
    @staticmethod
    def load_configuration():
        try:
            with open(Configuration.CONFIG_FILE,'r') as f:
                json_string = json.load(f)
                if not json_string or json_string['client_id']:
                    return 
                Configuration.CLINET_ID = json_string['client_id']
        except IOError:
            Configuration.CLINET_ID=None
    @staticmethod
    def set_client_id(client_id):
        print('set client id')
        Configuration.CLINET_ID = client_id
        Configuration.save_configuration()

    @staticmethod
    def save_configuration():

        with open(Configuration.CONFIG_FILE,'w') as f:
            json_string = {'client_id':Configuration.CLINET_ID}
            json.dump(json_string,f)

    @staticmethod 
    def get_ip_address():
        if Configuration.LOCAL_IP == None:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            Configuration.LOCAL_IP = s.getsockname()[0]
        return Configuration.LOCAL_IP



    @staticmethod 
    def get_indexed_folders():
        return Configuration.INDEXED_FOLDERS
        
    @staticmethod
    def get_client_id():
        if not Configuration.CLINET_ID:
            Configuration.load_configuration()
        return Configuration.CLINET_ID

    


