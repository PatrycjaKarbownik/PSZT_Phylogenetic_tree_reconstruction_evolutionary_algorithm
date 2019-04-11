import csv


def load():
    years = []
    names = []
    with open('../data/usflu.annot.csv', 'r', encoding='utf-8') as file1:
        csvreader = csv.reader(file1, delimiter=',')
        for row in csvreader:
            row[0].split(',')
            if (row[2] != "year"):
                years.append(row[2])
                names.append(row[1])
        file1.close()

    sequence = ""
    n = 0
    boolvar = False
    result1 = open("../data/result1.txt", "w")
    result2 = open("../data/result2.txt", "w")
    result3 = open("../data/result3.txt", "w")
    with open("../data/influenza.fna", "r") as file2:
        for line in file2:
            if n < 20:
                if not boolvar:
                    for i, name in enumerate(names):
                        if name in line:
                            boolvar = True
                            k = i
                elif ('>' in line):
                    boolvar = False
                    result1.write(names[k]+" "+years[k]+"\n"+sequence+"\n")
                    n += 1
                    sequence = ""
                elif boolvar:
                    sequence += line.rstrip('\n').upper()
                else:
                    pass
            elif n < 40:
                if not boolvar:
                    for i, name in enumerate(names):
                        if name in line:
                            boolvar = True
                            k = i
                elif ('>' in line):
                    boolvar = False
                    result2.write(names[k] + " " + years[k] + "\n" + sequence + "\n")
                    n += 1
                    sequence = ""
                elif boolvar:
                    sequence += line.rstrip('\n').upper()
                else:
                    pass
            elif n < 60:
                if not boolvar:
                    for i, name in enumerate(names):
                        if name in line:
                            boolvar = True
                            k = i
                elif ('>' in line):
                    boolvar = False
                    result3.write(names[k]+" "+years[k]+"\n"+sequence+"\n")
                    n += 1
                    sequence = ""
                elif boolvar:
                    sequence += line.rstrip('\n').upper()
                else:
                    pass
    file2.close()
    result1.close()
    result2.close()
    result3.close()
load()
