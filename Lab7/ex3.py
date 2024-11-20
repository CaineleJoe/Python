import os
import sys

from conda.exceptions import DirectoryNotFoundError


def directory_size(directory_path):
    try:
        if not os.path.isdir(directory_path):
            raise DirectoryNotFoundError(f"{directory_path} is invalid")
        total=0
        for root,dirs,files in os.walk(directory_path):
            try:
                for file in files:
                    total=total+ os.path.getsize(os.path.join(root,file))
            except Exception as e:
                print(f"{e} occured for {file}.")
        return total
    except Exception as e:
        print(e)

if len(sys.argv)!=2:
    print("Usage: python ex3.py <directory_path>")
    print(directory_size(sys.argv[1]))
    