# ex1
def operatii(x, y):
    print(x.union(y))
    print(x.intersection(y))
    print(x.difference(y))
    print(y.difference(x))


a = {1, 2, 3, 4}
b = {1, 3, 4, 5, 6}
operatii(a, b)


# ex2
def mapping(x):
    char_dict = {}
    for k in x:
        char_dict[k] = char_dict.get(k, 0) + 1
    return char_dict


print(mapping("Ana has apples."))


# ex3

def compare(d1, d2):
    if d1.keys() != d2.keys():
        return False
    for key in d1:
        val1 = d1[key]
        val2 = d2[key]
        if isinstance(val1, dict) and isinstance(val2, dict):
            if not compare(val1, val2):
                return False
        elif isinstance(val1, (list, set, tuple)) and isinstance(val2, (list, set, tuple)):
            if type(val1) != type(val2) or len(val1) != len(val2):
                return False
            if sorted(val1) != sorted(val2):
                return False

        else:
            if (val1 != val2):
                return False
    return True


dict1 = {
    'x': 10,
    'y': {'z': 20, 'w': [4, 5, 6]},
    'v': {7, 8, 9},
    'u': (1, 2, 3)
}

dict2 = {
    'x': 10,
    'y': {'z': 20, 'w': [4, 5, 6]},
    'v': {7, 8, 9},
    'u': (1, 2, 3)
}
dict3 = {
    'x': 10,
    'y': {'z': 20, 'w': [4, 5, 6], 'extra': 15},
    'v': {7, 8, 9},
    'u': (1, 2, 3)
}
print(compare(dict1, dict2))
print(compare(dict1, dict3))


# ex4
def build_xml_element(tag, content, **attributes):
    attributes_string = ''.join(f' {key}="{value}"' for key, value in attributes.items())

    xml_element = f"<{tag}{attributes_string}>{content}</{tag}>"
    return xml_element


print(build_xml_element("a", "Hello there", href="http://python.org", _class="my-link", id="someid"))


# ex5
def validate_dict(rules, dict):
    for key, preffix, middle, suffix in rules:
        if key not in dict:
            return False
        value = dict[key]
        if not value.startswith(preffix):
            return False
        if middle not in value[1:-1]:
            return False
        if not value.endswith(suffix):
            return False
    rule_keys = set(key for key, _, _, _ in rules)
    if not rule_keys >= dict.keys():
        return False
    return True


s = {("key1", "", "inside", ""), ("key2", "start", "middle", "winter")}
d = {"key1": "come inside, it's too cold out", "key3": "this is not valid"}
print(validate_dict(s, d))


# ex6

def count_unique_and_duplicates(lst):
    unique_elements = set(lst)
    total_unique = len(unique_elements)
    total_duplicates = len(lst) - total_unique

    return (total_unique, total_duplicates)


print(count_unique_and_duplicates([1, 2, 3, 3, 4, 4, 6, 5, 6]))


# ex7
def pairwise_set_operations(*sets):
    result = {}
    for i, set_a in enumerate(sets):
        for j, set_b in enumerate(sets):
            if i < j:
                result[f"{set_a} | {set_b}"] = set_a | set_b
                result[f"{set_a} & {set_b}"] = set_a & set_b
                result[f"{set_a} - {set_b}"] = set_a - set_b
                result[f"{set_b} - {set_a}"] = set_b - set_a
    return result


print(pairwise_set_operations({1, 2}, {2, 3})
      )


# ex8
def loop(mapping):
    result = []
    visited = set()

    current = mapping.get("start")
    while current not in visited:
        result.append(current)
        visited.add(current)
        current = mapping.get(current)

    return result


print(loop({'start': 'a', 'b': 'a', 'a': '6', '6': 'z', 'x': '2', 'z': '2', '2': '2', 'y': 'start'}))


# ex9
def counter(*args, **vals):
    keyword_values = set(vals.values())
    count = 0
    for arg in args:
        if arg in keyword_values:
            count = count + 1
    return count


print(counter(1, 2, 3, 4, x=1, y=2, z=3, w=5))
