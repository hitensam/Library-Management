# SOURCE https://gist.github.com/JeffPaine/3145490
import requests
import json


PROJECT_VERSIONS = {
    "molstar": {
        "owner": "molstar",
        "repo": "molstar",
        "custom_repo": "molstar",
        "release": "v3.32.0",
    },
    "indgio": {
        "owner": "epam",
        "repo": "indigo",
        "custom_repo": "Indigo",
        "release": "indigo-1.0.7",
    },
    "ketcher": {
        "owner": "epam",
        "repo": "ketcher",
        "custom_repo": "Ketcher",
        "release": "v2.7.2",
    },
}

RELEASES_URL = "https://api.github.com/repos/{owner}/{repo}/releases"
ISSUE_URL = "https://api.github.com/repos/{owner}/{repo}/issues"
ISSUES_ADD_LABEL = "https://api.github.com/repos/{owner}/{repo}/issues/{issue_id}"
ORGANIZATION = "QuanMol"
TOKEN = ""  # This is the PAT token

headers = {"Authorization": f"token {TOKEN}", "Accept": "application/vnd.github+json"}

# Create an authenticated session to create the issue
session = requests.Session()
session = requests.Session()
session.auth = ("luna215", TOKEN)


def add_label_to_issue(custom_repo: str, issue_id: str):
    labels = {"labels": ["P0 - Critical"]}
    session.post(
        ISSUES_ADD_LABEL.format(
            owner=ORGANIZATION, repo=custom_repo, issue_id=issue_id
        ),
        data=json.dumps(labels),
    )
    print(f"Labels added to issue {issue_id}")


def create_update_issue(latest_release: str, current_release: str, custom_repo: str):
    """Create an issue that describes to update the project"""

    issue = {
        "title": f"Update package to {latest_release}!",
        "body": f"The package is currently using {current_release} and we need to update it to {latest_release}",
    }
    response = session.post(
        ISSUE_URL.format(owner=ORGANIZATION, repo=custom_repo), data=json.dumps(issue)
    ).json()
    issue_id = response["number"]

    add_label_to_issue(custom_repo, issue_id)


if __name__ == "__main__":
    for project_name, project_info in PROJECT_VERSIONS.items():
        owner = project_info["owner"]
        repo = project_info["repo"]
        custom_repo = project_info["custom_repo"]
        current_release = project_info["release"]

        response = requests.get(RELEASES_URL.format(owner=owner, repo=repo))

        data = response.json()

        latest_release = data[0]["tag_name"]

        if latest_release != current_release:
            # TODO: check if issue exists to update project

            print(
                f"{project_name} needs to be updated! {current_release} --> {latest_release}"
            )
            create_update_issue(latest_release, current_release, custom_repo)
