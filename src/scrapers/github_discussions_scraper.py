import requests
import json
import os
from dotenv import load_dotenv

GITHUB_GRAPHQL_URL = "https://api.github.com/graphql"
MLOPS_REPOS = [
    "mlflow/mlflow",
    # "kubeflow/kubeflow",
    # "tensorflow/tensorflow",
    # "huggingface/transformers",
    # "DataTalksClub/mlops-zoomcamp",
    # "zenml-io/zenml"
]

GITHUB_DISCUSSIONS_QUERY = """
query ($owner: String!, $repo: String!, $cursor: String) {
  repository(owner: $owner, name: $repo) {
    discussions(first: 10, after: $cursor) {
      pageInfo {
        endCursor
        hasNextPage
      }
      nodes {
        title
        bodyText
        createdAt
        author {
          login
        }
        comments(first: 5) {
          nodes {
            bodyText
            author {
              login
            }
            createdAt
          }
        }
      }
    }
  }
}
"""

load_dotenv(dotenv_path=".env.local")

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    raise ValueError("GITHUB_TOKEN is missing! Add it to your .env file")

def fetch_github_discussions(owner, repo):
    discussions = []
    cursor = None

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Content-Type": "application/json"
    }

    while True:
        variables = {"owner": owner, "repo": repo, "cursor": cursor}
        response = requests.post(GITHUB_GRAPHQL_URL, json={"query": GITHUB_DISCUSSIONS_QUERY, "variables": variables}, headers=headers)

        if response.status_code != 200:
            print(f"Failed to fetch data for {repo}: {response.text}")
            break

        data = response.json()
        repo_data = data.get("data", {}).get("repository", {}).get("discussions", {})

        if "nodes" in repo_data:
            discussions.extend(repo_data["nodes"])

        if repo_data["pageInfo"]["hasNextPage"]:
            cursor = repo_data["pageInfo"]["endCursor"]
        else:
            break

    return discussions


def scrape_mlops_discussions():
    all_discussions = []

    for repo in MLOPS_REPOS:
        owner, repo_name = repo.split("/")
        print(f"Fetching discussions from {repo}...")
        discussions = fetch_github_discussions(owner, repo_name)
        all_discussions.extend(discussions)

    with open("data/github/github_mlops_discussions.json", "w") as f:
        json.dump(all_discussions, f, indent=4)

    print(f"Saved {len(all_discussions)} discussions to data/github/github_mlops_discussions.json")

if __name__ == "__main__":
    scrape_mlops_discussions()
