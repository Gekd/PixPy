from github import Github
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv("GITHUB_TOKEN")

repo_name = "Gekd/PixPy"
file_path = "test.txt"
commit_message = "Python script Test"

# Get today's date
current_date = datetime.now().strftime("%Y-%m-%d")
g = Github(token)

repo = g.get_repo(repo_name)

# Check if the folder for the current date exists
contents = repo.get_contents("uploads")

folder_exists = False

for content in contents:
    if content.type == "dir" and content.path == current_date:
        folder_exists = True
        break

# If the folder doesn't exist, create it
if not folder_exists:
    repo.create_file(f"uploads/{current_date}/.gitkeep", "Create date folder", "")
    print(f"Folder '{current_date}' created.")


with open(file_path, 'r', encoding='utf-8') as file:
    data = file.read()

# Create file
repo.create_file(f"uploads/{current_date}/{file_path.rsplit('/', maxsplit=1)[-1]}", commit_message, data)



print(f"File '{file_path.split('/')[-1]}' uploaded successfully to folder '{current_date}'.")