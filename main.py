import requests
import click

from diagram import build_diagram


def _get_authors_activity(username, token, organisation):
    authors_activity = {}
    repos_info = requests.get(
        f'https://api.github.com/orgs/{organisation}/repos',
        auth=(username, token)).json()
    for repo_info in repos_info:
        commits_url = repo_info["commits_url"][:-6]
        commits_info = requests.get(commits_url, auth=(username, token)).json()
        for full_commit_info in commits_info:
            try:
                commit_info = full_commit_info["commit"]
            except TypeError:
                continue
            author_email = commit_info["author"]["email"]
            if author_email not in authors_activity.keys():
                authors_activity[author_email] = 1
            else:
                authors_activity[author_email] += 1
    return authors_activity


@click.command(help='Gets max commits count author of the organisation')
@click.argument('organisation', required=True)
@click.argument('username', required=False)
@click.argument('token', required=False)
@click.option('-d', '--diagram', 'diagram', is_flag=True, required=False,
              help='Show diagram')
def get_max_commit_count_author(organisation, username, token, diagram):
    authors_activity = _get_authors_activity(username, token, organisation)
    if diagram:
        build_diagram(authors_activity)
    max_commits_count = 0
    max_commits_author = ''
    for author in authors_activity:
        if authors_activity[author] > max_commits_count:
            max_commits_count = authors_activity[author]
            max_commits_author = author
    click.echo((max_commits_author, max_commits_count))


if __name__ == '__main__':
    # token = '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'
    get_max_commit_count_author()
