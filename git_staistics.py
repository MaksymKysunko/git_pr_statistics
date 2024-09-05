import requests
from datetime import datetime
import csv
import os

# Get the token from the environment variable
token = os.getenv('GIT_HUB_TOKEN')

# Define your headers with the token
headers = {
    'Authorization': f'token {token}',
    'Accept': 'application/vnd.github.v3+json'
}

def getListOfRepos(userName : str):
  urlToRepos = f"https://api.github.com/orgs/{userName}/repos?per_page=100&page=1"
  repos=requests.get(urlToRepos, headers=headers).json()
  for repo in repos:
    print(repo["full_name"])

def getPullStatistics(repoName : str):
  urlToPulls = f"https://api.github.com/repos/rabotaua/{repoName}/pulls"
  final_dataset = []
  fmt = "%Y-%m-%dT%H:%M:%SZ"
  page = 1
  repos=[]
  while True:
    print(f"processing page {page}")
    res=requests.get(f"{urlToPulls}?state=closed&per_page=100&page={page}",headers=headers)
    if res.json() != []:
      repos.extend(res.json())
      page= page + 1
    else:
      break

  print("Fetching PRs, Please Wait")
  for data in repos:
    result = {}
    created_at = datetime.strptime(data['created_at'], fmt)
    closed_at = datetime.strptime(data['closed_at'], fmt)

    result['hours_to_review'] = round((closed_at - created_at).total_seconds() / 3600, 2)
    url_for_pr = (f"{urlToPulls}/{data['number']}")
    res=requests.get(url_for_pr,headers=headers)
    result['line_of_code'] = res.json()['additions']
    result['user_name'] = res.json()['user']['login']
    result['pr_number'] = data['number']
    print(f"Processing PR {data["number"]}")
    final_dataset.append(result)


  print("Writing to csv, Please Wait")
  keys = final_dataset[0].keys()
  with open(f'pr_review_data_{repoName}.csv', 'w', newline='') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(final_dataset)


#getPullStatistics("mavis")
getListOfRepos("rabotaua")
print("*************DONE*****************")