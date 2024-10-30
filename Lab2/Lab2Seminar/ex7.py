def nrUpper(x):
    count=0
    for i in x:
        if str(i).isupper():
            count=count+1
    return count
print(nrUpper("AM o mInge"))