from testrail import *
from project import Project
from run import Run

def close_run(run_id):
    close_run = client.send_post(f'close_run/{run_id}', {})
    print(close_run)

client = APIClient('https://mmoya26.testrail.io/')
client.user = 'mmoya18@icloud.com'
client.password = 'password123'

mainProject = None
project = client.send_get('get_projects')

projects = []

for item in project:
    projectItem = Project(item["id"], item["name"], item["announcement"], item["show_announcement"], item["is_completed"],
    item["completed_on"], item["suite_mode"], item["url"])
    projects.append(projectItem)

for project in projects:
    if project.name == "TEST PROJECT":
        mainProject = project


test_runs = client.send_get(f'get_runs/{mainProject.id}')
runs = []

for run in test_runs:
    r = Run(run["id"], run["name"], run["is_completed"], run["project_id"], run["suite_id"], run["url"])

    if not run["is_completed"]:
        runs.append(r)


close_run(runs[0].id)

