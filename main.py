import requests
import click
from time import perf_counter
from urllib.parse import quote

from diagram import build_diagram


def _process_commits_info(commits_info, authors_activity):
    for full_commit_info in commits_info:
        try:
            commit_info = full_commit_info["commit"]
        except TypeError:
            continue
        if "Merge pull request #" in commit_info["message"]:
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
            f'https://api.github.com/orgs/{quote(organisation)}/repos'
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


def _get_top_commits_count_authors(authors_activity, top_count=100):
    authors_activity_tuples = []
    for author in authors_activity:
        authors_activity_tuples.append((author, authors_activity[author]))
    authors_activity_tuples.sort(key=lambda pair: pair[1], reverse=True)
    top_commits_authors = authors_activity_tuples[:top_count]
    return top_commits_authors


@click.command(help='Gets max commits count author of the organisation')
@click.argument('organisation', required=True)
@click.option('-d', '--diagram', 'diagram', is_flag=True, required=False,
              default=False, help='Show diagram')
@click.argument('username', required=False, default=None)
@click.argument('token', required=False, default=None)
def main(organisation, diagram, username, token):
    authors_activity = _get_authors_activity(username, token, organisation)
    top_commits_authors = _get_top_commits_count_authors(authors_activity)
    if diagram:
        build_diagram(top_commits_authors, organisation)
    for author in top_commits_authors:
        click.echo(author)


if __name__ == '__main__':
    main()
