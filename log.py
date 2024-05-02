import json
import os
from datetime import datetime

def logJson(dataheading, data, filepath):
    file = open(filepath, 'w')
    file.write(json.dumps(dataheading))
    file.write(data.candidates)
    file.close()

def logText(text,filepath, data):
    if data['exists']:
        TestNum = get_test_file_number(filepath)
        file = open(filepath+ f'/test{TestNum-1}', 'w')
        file.write(text)
        file.close()
    else:
        TestNum = get_test_file_number(filepath)
        file = open(filepath+ f'/test{TestNum}', 'w')

        with open(data['source'], 'r') as src:
            file.write(
                        f'''Test N{TestNum} \t {datetime.now()} 
                        Prompt :  {data['prompt']}


                        The input text: 
                        {src.read()}
                        \n

                        --------------------Reformulation----------------
                        {text}
                        '''
                    )
        file.close()
        
def get_test_file_number(directory):
    # Get a list of all files in the directory
    files = os.listdir(directory)
    
    # Filter out directories, leaving only files
    files = [file for file in files if os.path.isfile(os.path.join(directory, file))]
    
    # Sort the files based on their creation time
    files.sort(key=lambda x: os.path.getctime(os.path.join(directory, x)))
    
    # Get the last file in the sorted list
    last_file = files[-1]
    c = ''
    for i in last_file:
        if i.isdigit():
            c = c + i
    
    return int(c) + 1