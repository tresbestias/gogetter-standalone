
import json

class Configuration():

    CLINET_ID = None

    CONFIG_FOLDER = './settings'
    CONFIG_FILE = CONFIG_FOLDER+'/settings.json'
    INDEXED_FOLDERS = ['/home/shibin/Documents/']
    # get the already stored client id
    @staticmethod
    def load_configuration():
        try:
            with open(Configuration.CONFIG_FILE,'r') as f:
                json_string = json.load(f)
                Configuration.CLINET_ID = json_string['client_id']
        except IOError:
            Configuration.CLINET_ID='not_set'
    @staticmethod
    def set_client_id(client_id):
        Configuration.CLINET_ID = client_id
        Configuration.save_configuration()

    @staticmethod
    def save_configuration():

        with open(Configuration.CONFIG_FILE,'w') as f:

            json_string = {'client_id':Configuration.CLINET_ID}
            json.dumps(json_string)



    @staticmethod 
    def get_indexed_folders():
        return Configuration.INDEXED_FOLDERS
        
    @staticmethod
    def get_client_id():
        if not Configuration.CLINET_ID:
            Configuration.load_configuration()
        return Configuration.CLINET_ID

    


