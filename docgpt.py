import argparse

from github.GithubDownloader import GithubDownloader
from parse.FilesParser import FilesParser
from generate.DocGptGenerator import DocGptGenerator
from upload.WikiUploader import WikiUploader

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Main script for downloading your repos and generation docs for them")

    parser.add_argument("repository_names", nargs='+', help="Repository names you want to work with")
    parser.add_argument("--download", action="store_true", help="Download data from your repo")
    parser.add_argument("--parse", action="store_true", help="Parse and prepare downloaded data")
    parser.add_argument("--generate", action="store_true", help="Generate docs output")
    parser.add_argument("--upload", action="store_true", help="Upload results")

    args = parser.parse_args()
    repo_names = args.repository_names

    if args.download:
        GithubDownloader(repo_names).download()
    if args.parse:
        FilesParser(repo_names).parse()
    if args.generate:
        DocGptGenerator(repo_names).generate_doc()
    if args.upload:
        WikiUploader(repo_names).upload()
