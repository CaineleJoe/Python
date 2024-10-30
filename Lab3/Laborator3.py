# ex1


def fibonacci(n):
    result = [0, 1]

    for i in range(2, n):
        next_val = result[i - 1] + result[i - 2]
        result.append(next_val)

    return result[:n]


print(fibonacci(4))


# ex2


def isPrime(n):
    for i in range(2, n):
        if n % i == 0:
            return False
    return True


def primeList(n):
    primeList = []
    for i in n:
        if isPrime(i):
            primeList.append(i)
    return primeList


print(primeList([12, 13, 14, 15, 16, 17, 18, 19]))


# ex3


def cardinals(a, b):
    intersection = []
    for i in a:
        if i in b:
            intersection.append(i)
    reunion = []
    for i in a:
        reunion.append(i)
    for i in b:
        if i not in reunion:
            reunion.append(i)

    a_red_b = []
    for i in a:
        if i not in b:
            a_red_b.append(i)

    b_red_a = []
    for i in b:
        if i not in a:
            b_red_a.append(i)

    return (
            "Reuniunea: "
            + str(reunion)
            + " Intersection: "
            + str(intersection)
            + " a-b: "
            + str(a_red_b)
            + " b-a: "
            + str(b_red_a)
    )


print(cardinals([1, 2, 3, 4, 5], [3, 4, 5, 6, 7]))


# ex4


def compose(musical_notes, moves, start):
    song = []
    song.append(musical_notes[start])
    for i in moves:
        song.append(musical_notes[(i + start) % len(musical_notes)])
        start = (i + start) % len(musical_notes)
    return song


print(compose(["do", "re", "mi", "fa", "sol"], [1, -3, 4, 2, -2, -8], 2))


# ex5
def matrix_0(matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    for i in range(0, rows):
        for j in range(0, cols):
            if i > j:
                matrix[i][j] = 0
    return matrix


print(matrix_0([[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]]))


# ex6

def multi_check(x, *lists):
    count = {}
    result = []
    for l in lists:
        for i in l:
            if i in count:
                count[i] += 1
            else:
                count[i] = 1
    for i in count:
        if count[i] == x:
            result.append(i)
    return result


print(multi_check(2, [1, 2, 3], [2, 3, 4], [4, 5, 6], [4, 1, "test"]))


# ex7

def isPalindrom(x):
    return str(x) == str(x)[::-1]


def getPalindroms(list):
    palindroms = 0
    max_palindrom = -9999
    for i in list:
        if isPalindrom(i):
            palindroms = palindroms + 1
            if i > max_palindrom:
                max_palindrom = i
    return (palindroms, max_palindrom)


print(getPalindroms([123, 456, 789, 10, 11, 22, 101]))


# ex8
def f(x=1, list=[], flag=True):
    big_list = []
    for string in list:
        sequence = []
        for i in range(len(string)):
            if ((ord(string[i]) % x == 0 and flag is True) or (ord(string[i]) % x != 0 and flag is False)):
                sequence.append(string[i])
        big_list.append(sequence)
    return big_list


x = 3
strings = ["abc", "def", "ghi", "jkl"]
flag = True
output = f(x, strings, flag)
print(output)


# ex9

def spectators(matrix):
    blocked_spectators = []
    for i in range(1, len(matrix)):
        for j in range(len(matrix[i])):
            for previous in range(0, i):
                if matrix[previous][j] >= matrix[i][j]:
                    blocked_spectators.append((i, j))
                    break
    return blocked_spectators


stadium_matrix = [
    [1, 2, 3, 2, 1, 1],
    [2, 4, 4, 3, 7, 2],
    [5, 5, 2, 5, 6, 4],
    [6, 6, 7, 6, 7, 5]
]
print(spectators(stadium_matrix))


# ex10
def combine(*lists):
    maxx = max(len(ls) for ls in lists)

    result = []
    for i in range(maxx):
        pair = []
        for ls in lists:
            if i < len(ls):
                pair.append(ls[i])
            else:
                pair.append(None)
        result.append(tuple(pair))
    return result


list1 = [1, 2, 3]
list2 = [5, 6, 7]
list3 = ["a", "b", "c"]
print(combine(list1, list2, list3))


# ex11
def order_tupples(x):
    return sorted(x, key=lambda y: y[1][2])


tuples_list = [('abc', 'bcd'), ('abc', 'zza')]
print(order_tupples(tuples_list))


# ex12
def rhyme(list):
    groups = []
    for elem in list:
        if len(elem) >= 2:
            rhyme = elem[-2:]
            found_group = False
            for group in groups:
                if group[0][-2:] == rhyme:
                    group.append(elem)
                    found_group = True
                    break
            if not found_group:
                groups.append([elem])

    return groups


words = ['ana', 'banana', 'carte', 'arme', 'parte']
print(rhyme(words))
