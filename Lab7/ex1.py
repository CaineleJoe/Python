import os
import sys

from conda.exceptions import DirectoryNotFoundError
from isapi import ExtensionError


def fileFinder(directory_path, extension):
    try:
        files_found=[]
        if not os.path.isdir(directory_path):
            raise DirectoryNotFoundError(f"{directory_path} is invalid")

        if not extension.startswith('.'):
            raise ExtensionError(f"{extension}is invalid")

        for root,dirs,files in os.walk(directory_path):
            for file in files:
                if file.endswith(extension):
                    files_found.append(os.path.join(root,file))

        if not files_found:
            print("No files found")
            return
        for file in files_found:
            try:
                y=open(file,'r')
                print(y.read())
            except Exception as e:
                print(f"{e} occured for {file}.")
    except Exception as e:
        print(e)
if len(sys.argv)!=3:
    print("Usage: python ex1.py <directory_path> <extension>")
    sys.exit(1)
    print(fileFinder(sys.argv[1],sys.argv[2]))
