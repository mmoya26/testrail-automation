from testrail import *
from project import Project
from run import Run
from suite import Suite
import argparse

# API URL connection + ADMIN user credentials
# This will need to be updated with the avalara testrail URL and an API user will need to be created for this specific process
# unless there is one already created it
client = APIClient('https://migueltestrail2.testrail.io/')
client.user = 'migueltestrail1@outlook.com'
client.password = 'Password123'

# Command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("--suite", help="Argument that will determine which Suite will be used to close all of its runs")
parser.add_argument("--project_id", help="Argument that will determine which Project will be used as a reference to look for suites and runs")
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

# IMPORTANT VARIABLES THAT WILL THE DETERMINE WHAT PROJECT, SUITE NAME, SUITE ID, WE ARE WORKING WITH
PROJECT_NAME = "Returns Excise"

# Checking if the --suite parameter value was provided (not empty)
if args.suite == None:
    print("--suite parementer was not provided, please try using --suite [suite_name]")
    quit()
else:
    SUITE_NAME = args.suite

# Checking if the --suite parameter value was provided (not empty)
if args.project_id == None:
    print("--project_id parementer was not provided, please try using --project_id [project_id]")
    quit()
else:
    PROJECT_ID = int(args.project_id)

# This variable will get automatically populated so no need to change
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
    print("Double check spelling for PROJECT_NAME variable or --project_id parameter or make sure is not empty")
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

if len(runs) == 0:
    print("Test Runs list is empty, no work to be done")
    quit()

close_run(runs)