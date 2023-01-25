import csv


def save_csv(name, lista):
    with open(f'{name}.csv', "w") as f:
        wr = csv.writer(f, delimiter=";")

        wr.writerow(list(lista[0].__dict__.keys()))
        for row in lista:
            wr.writerow(list(row.__dict__.values()))
