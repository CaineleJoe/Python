# ex1(ex1 usor)


def character_freq(r_file, w_file):
    paragraphs = open(r_file, 'r').read()
    char_freq = {}
    for char in paragraphs:
        if char.isalnum():
            if char.lower() not in char_freq:
                char_freq[char.lower()] = 0
            char_freq[char.lower()] += 1
    height = max(char_freq.values())
    histogram = []
    for i in range(height):
        line = []
        for value in char_freq.values():
            if value <= i:
                line.append('o')
            else:
                line.append(' ')
        histogram.append(line)
    histogram.append(char_freq.keys())
    open(w_file, 'w').write('\n'.join(''.join(line) for line in histogram))


character_freq('Luca.txt', 'Output.txt')

# ex2 (ex1greu)
import json


def calculeaza_nota_finala(student):
    seminarii = student["seminarii"]
    partial = student["partial"]
    curs = student["curs"]
    proiect = student["proiect"]

    media_seminarii = sum(seminarii) / len(seminarii)
    nota_seminarii = media_seminarii * 0.20
    nota_partial = (partial / 100) * 30
    nota_curs = (curs / 100) * 30
    nota_proiect = (proiect / 70) * 20

    nota_finala = nota_seminarii + nota_partial + nota_curs + nota_proiect

    return nota_finala


def calculeaza_rezultatele(fisier_json):
    with open(fisier_json, 'r') as f:
        studenti = json.load(f)

    studenti_trecuti = 0
    studenti_picati = 0

    for nume, student in studenti.items():
        nota_finala = calculeaza_nota_finala(student)
        print(nume, nota_finala)
        if nota_finala >= 45:
            studenti_trecuti += 1
        else:
            studenti_picati += 1

    return studenti_trecuti, studenti_picati


fisier_json = 'students.json'
studenti_trecuti, studenti_picati = calculeaza_rezultatele(fisier_json)

print(f"Studenți care au trecut: {studenti_trecuti}")
print(f"Studenți care au picat: {studenti_picati}")