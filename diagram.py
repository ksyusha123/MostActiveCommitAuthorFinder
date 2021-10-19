import matplotlib.pyplot as plt


def build_diagram(top_commits_authors, organisation):
    authors = []
    commits_counts = []
    commits_counts_sum = sum([commits_author[1]
                              for commits_author in top_commits_authors])
    for commits_author in top_commits_authors:
        if commits_author[1] > 0.03 * commits_counts_sum:
            authors.append(commits_author[0])
        else:
            authors.append('')
        commits_counts.append(commits_author[1])
    figure, ax = plt.subplots()
    ax.pie(commits_counts, labels=authors, labeldistance=None)
    ax.set_title(f"Commits authors for {organisation}")
    ax.legend(loc='upper left', bbox_to_anchor=(0.5, 1.0),
              title="Authors from top-100 that made at least 3%\nfrom "
                    "commits count shown by this diagram", labelspacing=0.1)
    figure.savefig('authors_activity_pie.png')
    plt.show()
