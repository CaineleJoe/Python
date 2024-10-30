def transform(x, alphabet):
    rest=0
    word=""
    while(x):
        rest=x%len(alphabet)
        x=x//len(alphabet)
        word=str(alphabet[rest])+word
    return word
print(transform(12,"abc"))