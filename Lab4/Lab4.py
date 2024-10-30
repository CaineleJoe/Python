#ex1
def operatii( x ,y):
    print(x.union(y))
    print(x.intersection(y))
    print(x.difference(y))
    print(y.difference(x))

a = {1,2,3,4}
b= {1,3,4,5,6}
operatii(a,b)

#ex2
def mapping(x):
    char_dict = {}
    for k in x:
        char_dict[k] = char_dict.get(k,0) + 1
    return char_dict
print(mapping("Ana has apples."))

#ex3

def compare(d1,d2):
    if d1.keys()!=d2.keys():
        return False
    for key in d1:
        val1=d1[key]
        val2=d2[key]
        if isinstance(val1,dict) and isinstance(val2,dict):
            if not compare(val1,val2):
                return False
        elif isinstance(val1,(list,set,tuple)) and isinstance(val2,(list,set,tuple)):
            if type(val1)!=type(val2) or len(val1)!=len(val2):
                return False
            if sorted(val1)!=sorted(val2):
                return False

        else:
            if (val1!=val2):
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
print(compare(dict1,dict2))
print(compare(dict1,dict3))

#ex4
def build_xml_element(tag, content, **attributes):
    attributes_string=''.join(f' {key}="{value}"' for key,value in attributes.items())

    xml_element = f"<{tag}{attributes_string}>{content}</{tag}>"
    return xml_element
print(build_xml_element("a", "Hello there", href="http://python.org", _class="my-link", id="someid"))

#ex5
def validate_dict(rules, dict):
    return True
