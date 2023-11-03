import json
import wget
import time
import csv
import requests
import math
from github.constants import OUTPUT_CSV_FILE, SUB_QUERIES, URL, QUERY, PARAMETERS, OUTPUT_FOLDER, DELAY_BETWEEN_QUERIES


class GithubDownloader:

    def __init__(self, repo_names):
        self.__repo_names = repo_names

    def download(self):
        print("######################################### DOWNLOADING ################################################")

        # To save the number of repositories processed
        count_of_repositories = 0

        # Output CSV file which will contain information about repositories
        csv_file = open(OUTPUT_CSV_FILE, 'w')
        repositories = csv.writer(csv_file, delimiter=',')

        # Run queries to get information in json format and download ZIP file for each repository
        for subquery in range(1, len(SUB_QUERIES) + 1):
            print("Processing subquery " + str(subquery) + " of " + str(len(SUB_QUERIES)) + " ...")
            # Obtain the number of pages for the current subquery (by default each page contains 100 items)
            url = URL + QUERY + str(SUB_QUERIES[subquery - 1]) + PARAMETERS
            data = json.loads(json.dumps(self.get_url(url)))
            number_of_pages = int(math.ceil(data['total_count'] / 100.0))
            print("No. of pages = " + str(number_of_pages))

            # Results are in different pages
            for current_page in range(1, number_of_pages + 1):
                print("Processing page " + str(current_page) + " of " + str(number_of_pages) + " ...")
                url = URL + QUERY + str(SUB_QUERIES[subquery - 1]) + PARAMETERS + "&page=" + str(current_page)
                data = json.loads(json.dumps(self.get_url(url)))
                # Iteration over all the repositories in the current json content page
                for item in data['items']:
                    # Obtain user and repository names
                    user = item['owner']['login']
                    repository = item['name']
                    # Skipping unnecessary repos
                    if repository not in self.__repo_names:
                        print(f"Repository {repository} not in REPOSITORY_NAMES script setting, skipping")
                        continue
                    # Download the zip file of the current project
                    print(f"Downloading repository {repository} from user {user}")
                    url = item['clone_url']
                    file_to_download = url[0:len(url) - 4] + "/archive/refs/heads/master.zip"
                    fileName = item['full_name'].replace("/", "#") + ".zip"
                    try:
                        wget.download(file_to_download, out=OUTPUT_FOLDER + fileName)
                        repositories.writerow([user, repository, url, "downloaded"])
                    except Exception as e:
                        print("Could not download file {}".format(file_to_download))
                        print(e)
                        repositories.writerow([user, repository, url, "error when downloading"])
                    # Update repositories counter
                    count_of_repositories = count_of_repositories + 1

            # A delay between different sub-queries
            if subquery < len(SUB_QUERIES):
                print("Sleeping " + str(DELAY_BETWEEN_QUERIES) + " seconds before the new query ...")
                time.sleep(DELAY_BETWEEN_QUERIES)

        print("DONE! " + str(count_of_repositories) + " repositories have been processed.")
        print("######################################################################################################")
        csv_file.close()

    @staticmethod
    def get_url(_url):
        """ Given a URL it returns its body """
        response = requests.get(_url)
        return response.json()
