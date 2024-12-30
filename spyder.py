"""
get all the input vectors by scanning/spidering
-cookies
-forms
-input vectors

forms with no action
-get all the input fields , check if label or just assign a random name
-find button with type=submit

check for sqli in all params
- ' breaks the app : status code changes 500(internal error),302(redirection)
- -- is comment
time delay,see if the html is returned after a delay

payloads
i)basic : on queries like ?administrator' OR 1=1--&password.. [pwd gets ignored]
"""

import time
import requests
import sys
from bs4 import BeautifulSoup
import json
 
from functionalities.spyder_ffuf import spyder_ffuf

dir_wordlist = 'wordlists/dirs.txt'
file = '/home/kali/Desktop/python_data/spyder/saved_data/save.json'

if __name__ == '__main__':
    s = requests.Session()
    url = sys.argv[1]
    recursive = int(sys.argv[2])
    #get_input(url)
    #check_sqli(url,action,inputs)
    #get_input(s,url)
    
    #initializing the classes
    """Link_obj = Link(url,session=s)
    urls = Link_obj.extract_urls()

    print(urls)
    for link in urls:
        Input_obj = Input(link)
        print(f'----Link:{link}-----')
        try:
            action,inputs = Input_obj.get_input(link)
            print(f'Action:{action} :: Input: {inputs}')
            save_data(link,action,inputs)
        except: 
            print('no inputs')"""
    
    #print(f'Action:{action} :: Input: {inputs}')

    fuzzer = spyder_ffuf(dir_wordlist,url,recursive)
    result = fuzzer.manager()
    result_json = fuzzer.tree_to_json(result)
    with open(file,'w') as f:
        f.write(json.dumps(result_json,indent=2))


