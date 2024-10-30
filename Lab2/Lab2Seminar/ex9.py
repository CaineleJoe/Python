def ex9(x):
    word=""
    for i in x.split():
        word=word+i[0]+ " "+ i[-1]+" "
    return word
print(ex9("am o chitara si o minge de baschet"))