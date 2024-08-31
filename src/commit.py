from github import Github
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import shutil

def github_commit(data):

    data = [item for sublist in data for item in sublist.split(", ")]

    load_dotenv()
    token = os.getenv("GITHUB_TOKEN")

    repo_name = "Gekd/PixPy"
    local_uploads_path = "src/uploads"
    commit_message = "Automated commit for the day"


    g = Github(token)
    repo = g.get_repo(repo_name)

    # 1. Check if "uploads" folder exists in local src folder
    if os.path.exists(local_uploads_path):
        # 2. Delete its contents
        shutil.rmtree(local_uploads_path)
        os.makedirs(local_uploads_path)
        print("Existing 'uploads' folder content deleted.")
    else:
        os.makedirs(local_uploads_path)
        print("No existing 'uploads' folder. Created a new one.")


    def get_date_from_day_number(year, day_number):
        # Create a datetime object for January 1st of the given year
        start_of_year = datetime(year, 1, 1)
        
        # Add the day number minus one (since day_number is 1-based) to the start_of_year
        target_date = start_of_year + timedelta(days=day_number - 1)
        
        # Return the date in "year-month-day" format
        return target_date.strftime("%Y-%m-%d")


    # 3. Get day number from year start and count today's pixel value
    today = datetime.now()
    day_of_year = today.timetuple().tm_yday

    print(f"Day of the year: {day_of_year}")
    day_count = 0

    for value in data:
        if value != "X":
            if day_count >= day_of_year:
                date = get_date_from_day_number(2024, day_count)
                
                # Create a date-time folder and file "commits.txt" with the number of commits for the day
                commits_file_path = os.path.join(local_uploads_path, date, "commits.txt")
                os.makedirs(os.path.dirname(commits_file_path), exist_ok=True)

                # Commit to commits.txt that day's pixel value
                with open(commits_file_path, 'w', encoding='utf-8') as file:
                    file.write(value)
            day_count += 1
                    


    # 4. Commit the "uploads" folder to GitHub
    """def upload_directory_to_github(local_dir, remote_dir, commit_msg):
        for root, _, files in os.walk(local_dir):
            for file in files:
                local_path = os.path.join(root, file)
                relative_path = os.path.relpath(local_path, local_dir)
                remote_path = os.path.join(remote_dir, relative_path)

                with open(local_path, 'r', encoding='utf-8') as f:
                    data = f.read()

                try:
                    repo.create_file(remote_path, commit_msg, data)
                    print(f"Uploaded {remote_path} to GitHub.")
                except Exception as e:
                    print(f"Failed to upload {remote_path}: {e}")

    upload_directory_to_github(local_uploads_path, "uploads", commit_message)"""

    print("All files committed to GitHub.")
    return True