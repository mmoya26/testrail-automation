from testrail import *
from project import Project
from run import Run
from suite import Suite

client = APIClient('https://mmoya18.testrail.io/')
client.user = 'nexonmiguel26@gmail.com'
client.password = 'Password123'

def close_run(runs):
    # Loop through runs list and send POST request to close all of the runs in it
    for run in runs:
        close_run = client.send_post(f'close_run/{run.id}', {})
        print(f'RunID {run.id}: was closed')
    
    print("################################################################################################################")

# IMPORTANT VARIABLES THAT WILL THE DETERMINE WHAT PROJECT, SUITE NAME, SUITE ID, WE ARE WORKING WITH
PROJECT_NAME = "Returns Excise"
SUITE_NAME = '5.43.10'
PROJECT_ID = 1
# No need to modify this variable
SUITE_ID = 0

# Variable that will hold our main project properties
mainProject = None

# Varaiable that will hold our main suite that we want to work with for the test runs
mainSuite = None

# List containing all of the runs
runs = []

# Gets all the projects from our testrail address
projectsList = client.send_get('get_projects')

for project in projectsList:
    #print(f'Current project name: {project["name"]}')
    if project["name"] == PROJECT_NAME and project["id"] == PROJECT_ID:
        # Create Project instance
        mainProject = Project(project["id"], project["name"], project["announcement"], project["show_announcement"], project["is_completed"],
        project["completed_on"], project["suite_mode"], project["url"])

        print(f'Main Project Name: {mainProject.name}')
        print("################################################################################################################")

# If main project is empty then do not continue with the rest of the program
# Double check spelling of variable PROJECT_NAME
if mainProject == None:
    print("Double check spelling for PROJECT_NAME or make sure is not empty")
    quit()

# Gets all the suites in our mainProject
# use mainProject.id as part of the API get call
suiteList = client.send_get(f'get_suites/{mainProject.id}')

# Loop through the suites
for suite in suiteList:
    s = Suite(suite["description"], suite["id"], suite["name"], suite["project_id"], suite["url"])
    # If the suite.project_id is the same as our mainAProject.id the add it to the suites list
    if s.project_id == mainProject.id:
        if s.name == SUITE_NAME:
            mainSuite = s
            SUITE_ID = s.id
            print(f'Main Suite Name: {s.name}')
print("################################################################################################################")

if mainSuite == None:
    print("Double check spelling for SUITE_NAME or make sure is not empty")
    quit()

# Gets all the currents runs in our mainProject
# use mainProject.id as part of the API get call
test_runs = client.send_get(f'get_runs/{mainProject.id}')

# Loop through the runs
for run in test_runs:
    # Create a temporary run instance
    r = Run(run["id"], run["name"], run["is_completed"], run["project_id"], run["suite_id"], run["url"])
    
    # print(r.id)
    # print(r.is_completed)
    # print(r.suite_id)
    # If run is not completed/close and belong to the main project and it is within the suite that we are working with
    # add that run to our runs list
    if r.is_completed == False and r.project_id == mainProject.id and r.suite_id == SUITE_ID:
        runs.append(r)
        print(f'RunID {r.id}: was added to "runs" list. Current lenght of "runs" list is: {len(runs)}')
print("################################################################################################################")

if len(runs) == 0:
    print("Test Runs list is empty, no work to be done")
    quit()

close_run(runs)