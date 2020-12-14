from testrail import *
from project import Project
from run import Run
from suite import Suite

def close_run(runs):
    
    # Loop through runs list and send POST request to close all of the runs in it
    for run in runs:
        close_run = client.send_post(f'close_run/{run.id}', {})
        print(close_run)

client = APIClient('https://mmoya26.testrail.io/')
client.user = 'mmoya18@icloud.com'
client.password = 'password123'
suite_name = 'Master'

mainProject = None
project = client.send_get('get_projects')


# List containing all of the projects
projects = []

# List containing all of the runs
runs = []

# List containing all of the suites
suites = []

for item in project:
    # Create Project instance
    projectItem = Project(item["id"], item["name"], item["announcement"], item["show_announcement"], item["is_completed"],
    item["completed_on"], item["suite_mode"], item["url"])

    # Add projectItem to projects list
    projects.append(projectItem)

for project in projects:

    # If the name of the project is the one that we are looking for
    if project.name == "TEST PROJECT":
        # Set our mainProject variable to be that project
        mainProject = project



suiteList = client.send_get(f'get_suites/{mainProject.id}')

for suite in suiteList:
    s = Suite(suite["description"], suite["id"], suite["name"], suite["project_id"], suite["url"])
    


# Gets all the currents runs in our mainProject
# use mainProject.id as part of the API get call
test_runs = client.send_get(f'get_runs/{mainProject.id}')

# Loop through the runs
for run in test_runs:
    # Create a temporary run instance
    r = Run(run["id"], run["name"], run["is_completed"], run["project_id"], run["suite_id"], run["url"])
    
    # If run is not completed/close and belong to the main project 
    if not run["is_completed"] and run["project_id"] == mainProject.id and run:
        print(f'{r.id} + {r.name}')
        # Add run to runs list
        runs.append(r)


