import matplotlib.pyplot as plt


def build_diagram(authors_activity):
    authors_activity_tuples = []
    authors = []
    commits_counts = []
    commits_counts_sum = sum(authors_activity.values())
    for author in authors_activity:
        if authors_activity[author] / commits_counts_sum < 0.05:
            authors.append('')
        else:
            authors.append(author)
        commits_counts.append(authors_activity[author])
        authors_activity_tuples.append((author, commits_counts))
    authors_activity_tuples.sort(key=lambda pair: pair[1], reverse=True)
    explode = tuple([0.1] + [0] * (len(authors_activity_tuples) - 1))
    figure, ax = plt.subplots()
    ax.pie(commits_counts, explode=explode, labels=authors)
    figure.savefig('authors_activity_pie.png')
    plt.show()
