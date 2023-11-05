import json
import os
import openai

from parse.constants import EXTRACT_FOLDER, PACKAGE_SOURCE_MAP_FILE
from generate.prompts import *


class DocGptGenerator:
    def __init__(self, repository_names):
        self.__repo_names = repository_names
        self.__openai_key = os.getenv("OPENAI_API_KEY")

    def generate_doc(self):
        # Read json with package names
        json_file_name = EXTRACT_FOLDER + PACKAGE_SOURCE_MAP_FILE
        if not os.path.exists(json_file_name):
            print(f"Error: no package source map file {json_file_name} found, exiting")
            exit()

        with open(json_file_name, 'r') as json_file:
            package_map = json.load(json_file)

        print("######################################### GENERATING ################################################")
        # Ask gpt the initial question
        initial_question = INITIAL_PROMPT + SOURCES_EXTENSION_HINT + 'python'
        print(initial_question)
        print(f"{self.__get_response_from_gpt(initial_question)}")
        # Ask gpt about files
        for package, files in package_map.items():
            if package.split("-")[0] not in self.__repo_names:
                print(f"Package: {package} not in repo_names, skipping")
                continue
            for file in files:
                self.__ask_gpt_about_file(file)
        # Ask gpt final question
        print(f"{self.__get_response_from_gpt(GENERAL_QUESTION)}")

    def __ask_gpt_about_file(self, file):
        file_question = FILE_QUESTION + file
        print(f"{self.__get_response_from_gpt(file_question)}")

    def __get_response_from_gpt(self, script):
        # Send a request to the model
        response = openai.Completion.create(
            engine="davinci",
            prompt=script,
            max_tokens=100,
            api_key=self.__openai_key
        )
        # Get the AI's response
        return response.choices[0].text
