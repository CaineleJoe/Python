def convert(x):
    binar=""
    while(x):
        binar=str(x%2)+binar
      
    if(binar):
        return "0b"+str(binar)
    return "0b0"
print(convert(4))
