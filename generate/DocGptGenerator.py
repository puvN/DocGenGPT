import json
import os

from parse.constants import EXTRACT_FOLDER, PACKAGE_SOURCE_MAP_FILE
from openai import OpenAI
from generate.prompts import CONSTANTS
from generate.settings import CURRENT_LANGUAGE


class DocGptGenerator:
    def __init__(self, repository_names):
        self.__repo_names = repository_names
        self.__openai_key = os.environ.get("OPENAI_API_KEY")
        self.__client = OpenAI()

    def generate_doc(self):
        # Read json with package names
        json_file_name = EXTRACT_FOLDER + PACKAGE_SOURCE_MAP_FILE
        if not os.path.exists(json_file_name):
            print(f"Error: no package source map file {json_file_name} found, exiting")
            exit()

        with open(json_file_name, 'r') as json_file:
            package_map = json.load(json_file)

        print("Generating docs...")
        # Ask gpt the initial question
        self.__get_response_from_gpt(CONSTANTS["INITIAL_PROMPT"][CURRENT_LANGUAGE])
        # Ask gpt about files
        for package, files in package_map.items():
            if package.split("-")[0] not in self.__repo_names:
                print(f"Package: {package} not in repo_names, skipping")
                continue
            for file in files:
                with open(file, 'r') as file_content:
                    file_question = CONSTANTS["FILE_QUESTION"][CURRENT_LANGUAGE] + file_content.read()
                    self.__get_response_from_gpt(file_question)
        # Ask gpt final question
        self.__get_response_from_gpt(CONSTANTS["GENERAL_QUESTION"][CURRENT_LANGUAGE])

    def __get_response_from_gpt(self, script):
        print(f"{script}\n")
        completion = self.__client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": "You are a system analyst who should analyze incoming files of a project and understand "
                            "what this project does."},
                {"role": "user", "content": script}
            ]
        )
        print(f"{completion.choices[0].message.content}\n")
