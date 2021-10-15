import requests
import click
from time import perf_counter

from diagram import build_diagram


def _process_commits_info(commits_info, authors_activity):
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


def _get_authors_activity(username, token, organisation):
    start = perf_counter()
    authors_activity = {}
    current_repos_page = 1
    while True:
        repos_info = requests.get(
            f'https://api.github.com/orgs/{organisation}/repos'
            f'?page={current_repos_page}',
            auth=(username, token)).json()
        if not repos_info:
            break
        for repo_info in repos_info:
            if not repo_info:
                break
            commits_url = repo_info["commits_url"][:-6]
            click.echo(commits_url)
            current_commits_page = 1
            while True:
                full_commits_info = requests.get(
                    f'{commits_url}?page={current_commits_page}',
                    auth=(username, token)).json()
                if not full_commits_info:
                    break
                _process_commits_info(full_commits_info, authors_activity)
                current_commits_page += 1
        current_repos_page += 1
    finish = perf_counter()
    click.echo(finish - start)
    return authors_activity


def _get_max_commits_count_author(authors_activity):
    max_commits_count = 0
    max_commits_author = ''
    for author in authors_activity:
        if authors_activity[author] > max_commits_count:
            max_commits_count = authors_activity[author]
            max_commits_author = author
    return max_commits_author, max_commits_count


@click.command(help='Gets max commits count author of the organisation')
@click.argument('organisation', required=True)
@click.option('-d', '--diagram', 'diagram', is_flag=True, required=False,
              default=False, help='Show diagram')
@click.argument('username', required=False, default=None)
@click.argument('token', required=False, default=None)
def main(organisation, diagram, username, token):
    authors_activity = _get_authors_activity(username, token, organisation)
    max_commits_author, max_commits_count = \
        _get_max_commits_count_author(authors_activity)
    if diagram:
        build_diagram(authors_activity)
    click.echo(f'{max_commits_author}: {max_commits_count}')


if __name__ == '__main__':
    # token = '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'
    main()
