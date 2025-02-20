import requests
import json
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env.local")
STACKOVERFLOW_API_KEY = os.getenv("STACKOVERFLOW_API_KEY")

if not STACKOVERFLOW_API_KEY:
    print("No API key found. Using limited public access.")

STACKOVERFLOW_API_URL = "https://api.stackexchange.com/2.3/questions"
MAX_RESULTS=5

MLOPS_TAGS = ["mlops", 
              #"mlflow", "kubeflow", "tensorflow-extended", "model-deployment"
             ]
def fetch_stackoverflow_questions(tag, max_results=MAX_RESULTS):
    params = {
        "order": "desc",
        "sort": "votes",
        "tagged": tag,
        "site": "stackoverflow",
        "pagesize": max_results,
        "filter": "withbody",
        "is_answered": "true"
    }
    if STACKOVERFLOW_API_KEY:
        params["key"] = STACKOVERFLOW_API_KEY

    response = requests.get(STACKOVERFLOW_API_URL, params=params)
    if response.status_code != 200:
        print(f"Failed to fetch data for tag '{tag}': {response.text}")
        return []
    
    return response.json().get("items", [])


def fetch_top_answers(question_id):
    answer_url = f"https://api.stackexchange.com/2.3/questions/{question_id}/answers"
    params = {
        "order": "desc",
        "sort": "votes",
        "site": "stackoverflow",
        "pagesize": 3,
        "filter": "withbody"
    }
    if STACKOVERFLOW_API_KEY:
        params["key"] = STACKOVERFLOW_API_KEY
    
    response = requests.get(answer_url, params=params)
    if response.status_code != 200:
        print(f"⚠️ Could not fetch answers for question {question_id}")
        return []
    
    answers = response.json().get("items", [])
    sorted_answers = sorted(answers, key=lambda x: (x.get("is_accepted", False), x["score"]), reverse=True)
    
    return [
        {
            "body": ans["body"],
            "score": ans["score"],
            "is_accepted": ans.get("is_accepted", False)
        }
        for ans in sorted_answers
    ]


def scrape_stackoverflow_mlops():
    all_questions = []
    for tag in MLOPS_TAGS:
        print(f"Fetching questions tagged with '{tag}'...")
        questions = fetch_stackoverflow_questions(tag)
        
        for q in questions:
            if not q.get("is_answered", False):
                continue  

            question_data = {
                "question_id": q["question_id"],
                "title": q["title"],
                "creation_date": q["creation_date"],
                "body": q["body"] if "body" in q else None,
                "tags": q["tags"],
                "score": q["score"],
                "link": q["link"],
                "top_answers": fetch_top_answers(q["question_id"])
            }
        
            all_questions.append(question_data)
    
    with open("data/stackoverflow/stackoverflow_mlops.json", "w") as f:
        json.dump(all_questions, f, indent=4)
    
    print(f"Saved {len(all_questions)} Stack Overflow MLOps discussions to data/stackoverflow/stackoverflow_mlops.json")

if __name__ == "__main__":
    scrape_stackoverflow_mlops()
