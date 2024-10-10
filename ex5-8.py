#ex5
def isPalindrom(x):
    return str(x)==str(x)[::-1]
x=121
print(isPalindrom(x))

#ex6
def firstNumber(x):
    number=""
    for i in x:
        if i.isdigit():
            number=number+i
        elif number:
            break
    if number:
        return number
    else:
        return "No number found"
print(firstNumber("luca123l4uca1"))

#ex7

def nrbiti1(x):
    bits1=0
    while(x):
        if(x%2==1):
            bits1=bits1+1
        x=x//2
    return int(bits1)

print(nrbiti1(7))

#ex8
def wordCounter(x):
    count=0
    for i in  x.split():
        count=count+1
    return count
print(wordCounter("salut     fram da     "))
