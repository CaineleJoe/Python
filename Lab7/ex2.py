import os
import sys
from conda.exceptions import DirectoryNotFoundError

def rename(directory_path):
    try:
        if not os.path.isdir(directory_path):
            raise DirectoryNotFoundError(f"{directory_path} is invalid")

        for root,dirs,files in os.walk(directory_path):
            i=0
            for file in files:
                i=i+1
                try:
                    os.rename(os.path.join(root,file),os.path.join(root,f"file{i}.png"))
                except Exception as e:
                    print(f"{e} occured for {file}.")


    except Exception as e:
        print(e)
        sys.exit(1)

rename("D:\\Poze Aquaterra\\pasari")