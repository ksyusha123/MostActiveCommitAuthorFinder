import matplotlib as mpl
import matplotlib.pyplot as plt

dpi = 80
figure = plt.figure(dpi=dpi, figsize=(4096 / dpi, 3072 / dpi))
mpl.rcParams.update({'font.size': 10})

plt.title('Commit authors activity')


def build_diagram(authors_activity):
    commits_count = list(authors_activity.values())
    commits_count.sort(key=lambda x: x, reverse=True)
    plt.bar(authors_activity.keys(), commits_count)
    figure.autofmt_xdate(rotation=90)
    figure.savefig('authors_activity.png')
