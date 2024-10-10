def occurences(x, y):
    count = 0
    i = 0

    while i <= len(y) - len(x):
        if y[i : i + len(x)] == x:
            count += 1
            i += 1
        else:
            i += 1
    return count


x = input("Substring: ")
y = input("String: ")
print(occurences(x, y))
