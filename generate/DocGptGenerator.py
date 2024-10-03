import json
import os

import requests

from parse.constants import EXTRACT_FOLDER, PACKAGE_SOURCE_MAP_FILE
from generate.prompts import CONSTANTS
from generate.Models import *
from generate.constants import *


class DocGptGenerator:
    def __init__(self, repository_names):
        self.__repo_names = repository_names
        self.__openai_key = os.environ.get("DOC_GEN_API_KEY")

    def generate_doc(self):
        # Read json with package names
        json_file_name = EXTRACT_FOLDER + PACKAGE_SOURCE_MAP_FILE
        if not os.path.exists(json_file_name):
            print(f"Error: no package source map file {json_file_name} found, exiting")
            exit()

        if not os.path.exists(DOCS_FOLDER):
            os.makedirs(DOCS_FOLDER)

        with open(json_file_name, 'r') as json_file:
            package_map = json.load(json_file)

        print("Generating docs...")
        # Ask gpt the initial question
        self.__get_response_from_gpt(CONSTANTS["INITIAL_PROMPT"][CURRENT_LANGUAGE])

        # TODO add multiple repos handled in generation
        doc_models = []
        # Ask gpt about files
        for package, files in package_map.items():
            repo_name = package.split("-")[0]
            if repo_name not in self.__repo_names:
                print(f"Repo name: {repo_name} not in repo_names, skipping")
                continue

            for file in files:
                with open(file, 'r') as file_content:
                    script_text = file_content.read()
                    file_question = CONSTANTS["FILE_QUESTION"][CURRENT_LANGUAGE] + script_text
                    gpt_response = self.__get_response_from_gpt(file_question)
                    doc_models.append(DocModel(file, script_text, gpt_response))

        # Ask gpt final question for package
        final_response = self.__get_response_from_gpt(CONSTANTS["GENERAL_QUESTION"][CURRENT_LANGUAGE])
        package_model = DocPackageModel(repo_name, doc_models, final_response)
        # Save on disk
        json_file_name = DOCS_FOLDER + repo_name + ".json"
        with open(json_file_name, "w") as json_file:
            json.dump(package_model.to_dict(), json_file, indent=4)

    def __get_response_from_gpt(self, script):
        print(f"{script}\n")
        api_url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.__openai_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": MODEL_NAME,
            "messages": [
                {"role": "system",
                 "content": "You are a system analyst who should analyze incoming files of a project and understand "
                            "what this project does."},
                {"role": "user", "content": script}
            ]
        }
        response = requests.post(api_url, json=data, headers=headers)

        if response.status_code == 200:
            response = response.json()["choices"][0]["message"]["content"]
            print("Response:\n", response)
        else:
            print("Error:", response.text)
        return response

