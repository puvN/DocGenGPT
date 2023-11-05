import json
import os.path

from parse.constants import EXTRACT_FOLDER, PACKAGE_SOURCE_MAP_FILE


class DocGptGenerator:
    def __init__(self, repository_names):
        self.__repo_names = repository_names

    def generate_doc(self):
        # Read json with package names
        json_file_name = EXTRACT_FOLDER + PACKAGE_SOURCE_MAP_FILE
        if not os.path.exists(json_file_name):
            print(f"Error: no package source map file {json_file_name} found, exiting")
            exit()
        package_map = {}
        with open(json_file_name, 'r') as json_file:
            package_map = json.load(json_file)

        for package, files in package_map.items():
            if package.split("-")[0] not in self.__repo_names:
                print(f"Package: {package} not in repo_names, skipping")
                continue
            for file in files:
                self.ask_gpt(file)

    @staticmethod
    def ask_gpt(file):
        print(f"asking gpb about {file}")