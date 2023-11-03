URL = "https://api.github.com/search/repositories?q="  # The basic URL to use the GitHub API
QUERY = "user:puvN"  # The personalized query (for instance, to get repositories from user 'rsain')
SUB_QUERIES = ["+created%3A>%3D2022-01-01"]  # Different sub-queries if you need to collect more than 1000 elements
PARAMETERS = "&per_page=100"  # Additional parameters for the query (by default 100 items per page)
DELAY_BETWEEN_QUERIES = 10  # The time to wait between different queries to GitHub (to avoid be banned)
OUTPUT_FOLDER = "C:\\Users\\Professional\\GitHub-Crawler\\"  # Folder where ZIP files will be stored
# Path to the CSV file generated as output
OUTPUT_CSV_FILE = "C:\\Users\\Professional\\GitHub-Crawler\\repositories.csv"
