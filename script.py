from testrail import *
from project import Project
from run import Run
from suite import Suite
import argparse

# API URL connection + ADMIN user credentials
client = APIClient('https://migueltestrail2.testrail.io/')
client.user = 'migueltestrail1@outlook.com'
client.password = 'Password123'

# Command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("--delete_by_user", help="Argument that will determine if we want to delete by user specific only, if so, please provide user email")
args = parser.parse_args()

def close_run(runs):
    # Loop through runs list and send POST request to close all of the runs in it
    for run in runs:
        try:
            close_run = client.send_post(f'close_run/{run.id}', {})
            print(f'RunID {run.id} - Run Name: {run.name} - was closed')
        except:
            print("Something went wrong when trying to close the runs, try again later.")
    
    print("################################################################################################################")

def get_runs(user):
    # Gets all the currents runs in our mainProject
    # use mainProject.id as part of the API get call
    try:
        test_runs = client.send_get(f'get_runs/{mainProject.id}')
    except:
        print("Something went wrong when trying to get the tests runs, try again later.")

    # If there is no user then do not print the following statement
    if user != None:
        print(f'Getting runs for: User Name: {user["name"]} - User Email: {user["email"]} - User ID: {user["id"]}')
        print(f"Getting runs from Suite: Suite ID: {SUITE_ID} - Suite Name: {SUITE_NAME}")
    else:
        print(f"Getting all runs from Suite: Suite ID: {SUITE_ID} - Suite Name: {SUITE_NAME}")

    print("################################################################################################################")

    # Loop through the runs
    for run in test_runs:
        # Create a temporary run instance
        r = Run(run["id"], run["name"], run["is_completed"], run["project_id"], run["suite_id"], run["created_by"], run["url"])
    
        if user != None:
            # If run is not completed/closed belong to the main project and it is within the suite that we are working with
            # and it mataches the user id from the provided user email then, add that run to our runs list
            if r.is_completed == False and r.project_id == mainProject.id and r.suite_id == SUITE_ID and r.created_by == int(user["id"]):
                runs.append(r)
                print(f'RunID {r.id}: was added to "runs" list. Current lenght of "runs" list is: {len(runs)}')
        else:
            # If run is not completed/closed and belong to the main project and it is within the suite that we are working with
            # add that run to our runs list
            if r.is_completed == False and r.project_id == mainProject.id and r.suite_id == SUITE_ID:
                runs.append(r)
                print(f'RunID {r.id}: was added to "runs" list. Current lenght of "runs" list is: {len(runs)}')


def  generate_runs():
    for x in range(20):
        create_runs = client.send_post(f'add_run/1', {"suite_id": 1, "name": f"Run {x}: Suite: {SUITE_NAME}", "assignedto_id": 1, "refs": "SAN-1, SAN-2",
	    "include_all": False, "case_ids": [1, 2]})


# IMPORTANT VARIABLES THAT WILL THE DETERMINE WHAT PROJECT, SUITE NAME, SUITE ID, WE ARE WORKING WITH
PROJECT_NAME = "Returns Excise"
SUITE_NAME = '5.43.10'
PROJECT_ID = 1
SUITE_ID = 0

# Variable that will hold our main project properties
mainProject = None

# Varaiable that will hold our main suite that we want to work with for the test runs
mainSuite = None

# List containing all of the runs
runs = []

# Gets all the projects from our testrail address\
try:
    projectsList = client.send_get('get_projects')
except:
    print("Something went wrong when trying to get the TestRail projects, try again later.")

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
try:
    suiteList = client.send_get(f'get_suites/{mainProject.id}')
except:
    print("Something went wrong when trying to get the Suites from TestRail, try again later.")

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

# Check if the user email was provided to delete runs by user only
# if it wasn't provided the method will add all of the runs for the suite to runs[]
# if it was provided the method 
if args.delete_by_user == None:
    get_runs(user=None)
else:
    try:
        user = client.send_get(f'/get_user_by_email&email={args.delete_by_user}')
        get_runs(user = user)
    except:
        print(f"The email: {args.delete_by_user} is not associated with any user in Testrail, try entering the email address again.")
        quit()

generate_runs()

if len(runs) == 0:
    print("Test Runs list is empty, no work to be done")
    quit()

#close_run(runs)
