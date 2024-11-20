import os
import sys

from conda.exceptions import DirectoryNotFoundError

from Lab4.Lab4 import dict1


def extensions_counter(directory_path):
    try:
        if not os.path.isdir(directory_path):
            raise DirectoryNotFoundError(f"{directory_path} is invalid")
        dict1={}
        for root,dirs,files in os.walk(directory_path):
            for file in files:
                try:
                    name,extention=file.split('.')
                    dict1[extention]+=1
                except Exception as e:
                    print(f"{e} occured for {file}.")
    except Exception as e:
        print(e)
    return dict1

if len(sys.argv)!=2:
    print("Usage: python ex4.py <directory_path>")
print(extensions_counter(sys.argv[1]))