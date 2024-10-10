def count_vowels(x):
    vowels = "aieouAEIOU"
    count = 0
    for char in x:
        if char in vowels:
            count += 1
    return count


text = input("Text: ")
print(count_vowels(text))
