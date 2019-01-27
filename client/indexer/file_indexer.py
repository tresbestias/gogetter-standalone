
import json 
import os
INDEX_FOLDER = os.path.dirname(os.path.realpath(__file__)) +'/indexinfo'
INDEX_FILE = INDEX_FOLDER+'/index.json'
import os
from Conf import Configuration
import sys
import time
import azure
"""

    index structure:

{
"nowTime":1548539690,
"updateCount":1,
"updateResult:[

{          "id": "d1/d2/asdasdf",
          "text": "asdfasdf",
          "type": "file/directory",
          "updateTime": 1548539690,
          "createTime": 1548539690
}
],
deleteCount:1,
deleteResult:["id1", "id2"],
owner:"deviceId"
}
"""

def store_index(file_ids):
    indexes = {}
    indexes['file_ids'] = file_ids
    
    with open(INDEX_FILE,'w') as f:
        print(indexes)
        json.dump(indexes,f)
    

def load_old_index():
    try:
        with open(INDEX_FILE,'r') as f:
            json_string = json.load(f,encoding="utf-8")
            return json_string['file_ids']
    except IOError:
        return []
    except ValueError:
        return []




def get_deleted_files(new_ids):
    old_index = load_old_index()
    new_ids = set([x.decode('utf-8') for x in new_ids ])

    delted_index = [ o_index for o_index in old_index if o_index not in new_ids]
    print(delted_index)
    return delted_index


def get_modified_files_dir_wise(folder,last_time):
    print(folder)
    all_files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(folder) for f in filenames]
    print(all_files)
    result = []
    
    for file in all_files:
        m_time = os.path.getmtime(file)
        if m_time>last_time:
            temp = {}
            temp['id'] = file
            temp['text'] =file.split('/')[-1]
            temp['type'] = 'file'
            temp['updateTime'] = int(m_time)
            temp['createTime'] = int(os.path.getctime(file))
            result.append(temp)

    return result,all_files

def get_modified_files(last_time):

    modified_folder = []
    all_ids = []
    for folder in Configuration.get_indexed_folders():
        temp_added,temp_all = get_modified_files_dir_wise(folder,last_time)
        modified_folder += temp_added
        all_ids += temp_all


    
    return modified_folder,all_ids


def get_new_indexing(last_time):
    
    modified_files,all_ids =  get_modified_files(last_time)
    deleted_ids = get_deleted_files(all_ids)

    result = {}

    result['nowTime'] = int( time.time())
    result['updateCount'] = len(modified_files)
    result['updateResult'] = modified_files
    result['deleteCount'] = len(deleted_ids)
    result['deleteResult'] = deleted_ids
    result['owner'] = Configuration.get_client_id()

    ## additional tags for image
    get_images_additional_info(modified_files)

    store_index(all_ids)
    return result

def get_images_additional_info(modified_files):
    
    formats = set(['jpg','png'])
    image_files = [ x for x in modified_files if x['text'].split('.')[-1] in formats ]
    
    for image in image_files:
        meta = azure.get_image_caption(image['id'])
        image['meta'] = meta
        


def get_file_link(file_id):
    return '/file?file='+file_id





    

    



    



    



