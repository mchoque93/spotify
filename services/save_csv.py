import csv

def save_csv(name, file):
    with open(f'{name}.csv', "w") as f:
        wr = csv.writer(f, delimiter="\n")
        wr.writerow(file)