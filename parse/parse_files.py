import csv
import zipfile
import os
import json
from typing import List

from github.constants import OUTPUT_CSV_FILE, OUTPUT_FOLDER
from parse.constants import FIELD_NAMES, EXTRACT_FOLDER, SRC_FILE_EXTENSION


class FilesParser:

    def __init__(self, repo_names):
        self.__repo_names = repo_names

    def parse(self):
        print("############################################# PARSING ################################################")
        # Read repositories csv file and filter data by downloaded and repo_names
        repo_file_names = self._get_downloaded_repo_names()
        # Search archived repos, unzip it, build a list of maps of
        package_source_map = self._get_sources_tree(repo_file_names)
        # Save result to json
        json_file_name = EXTRACT_FOLDER + "package_source_map.json"
        with open(json_file_name, "w") as json_file:
            json.dump(package_source_map, json_file, indent=4)
        print(f"DONE! check {json_file_name} for packages and files")
        print("######################################################################################################")

    @staticmethod
    def _get_sources_tree(repo_file_names):
        source_files = {}
        for repo in repo_file_names:

            with zipfile.ZipFile(OUTPUT_FOLDER + repo, 'r') as zip_ref:
                zip_ref.extractall(EXTRACT_FOLDER)

            for root, _, files in os.walk(EXTRACT_FOLDER):
                for file in files:
                    if file.endswith(SRC_FILE_EXTENSION):  # TODO add several extensions
                        package = root.replace(EXTRACT_FOLDER, "").replace(os.path.sep, ".").strip(".")
                        if package not in source_files:
                            source_files[package] = []
                        source_files[package].append(os.path.join(root, file))
        return source_files

    def _get_downloaded_repo_names(self) -> List[str]:
        with open(OUTPUT_CSV_FILE, 'r') as file:
            csv_reader = csv.DictReader(file, fieldnames=FIELD_NAMES)
            downloaded_repos = []
            for row in csv_reader:
                repo_name = row['repo_name']
                if row['downloaded'] != "downloaded":
                    print(f"Repository {repo_name} not downloaded, skipping")
                    continue
                if repo_name not in self.__repo_names:  # Make sure self.__repo_names is initialized correctly
                    print(f"Skipping downloaded repo {repo_name} because it is not selected")
                    continue
                author = row['author']
                downloaded_repos.append(author + "#" + repo_name + ".zip")
            print(f"Will handle repos: {downloaded_repos}")
        return downloaded_repos
