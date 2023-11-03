import argparse

from github.get_data_from_github import GithubDownloader
from parse.parse_files import FilesParser

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Main script for downloading your repos and generation docs for them")

    parser.add_argument("repository_names", nargs='+', help="Repository names you want to work with")
    parser.add_argument("--download", action="store_true", help="Download data from your repo")
    parser.add_argument("--parse", action="store_true", help="Parse and prepare downloaded data")
    parser.add_argument("--generate", action="store_true", help="Generate docs output")

    args = parser.parse_args()
    repo_names = args.repository_names

    if args.download:
        GithubDownloader(repo_names).download()
    if args.parse:
        FilesParser(repo_names).parse()
    if args.generate:
        print("argument is not implemented")
