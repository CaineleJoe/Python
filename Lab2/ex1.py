n=int(input("Introdu nr. de numere"))
l=[]
minv=-9999
divmax=1
for i in range (0,n):
    number=int(input("Introdu nr:"))
    l.append(number)
    if minv<abs(l[i]):
        minv=abs(l[i])
for i in range (minv,1,-1):
    alldiv=True
    for j in range (0,n):
        if l[j]%i!=0:
            alldiv=False
            break

    if alldiv==True:
        divmax=i
        break
print("Cel mai mare divizor comun este: "+ str(divmax))
