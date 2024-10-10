def convert(x):
    while len(str(x))%4!=0:
        x='0'+str(x)
    hex=""
    for i in range(0,len(str(x)),4):
        group=str(x)[i:i+4]
        number=0
        power=0 
        for bit in str(group)[::-1]:
            number=number+int(bit)*2**power
            power=power+1
        if number>9:
            number=chr(ord('A')+int(number)-10)
        hex=hex+str(number)
    return hex
print(convert(10111110000))