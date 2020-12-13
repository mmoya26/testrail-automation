from testrail import *
from project import Project

classProject = Project(2, 'project_test', None, False, False, None, 1, 'https://mmoya26.testrail.io/index.php?/projects/overview/1')
 
client = APIClient('https://mmoya26.testrail.io/')
client.user = 'mmoya18@icloud.com'
client.password = 'password123'

projects = []

project = client.send_get('get_projects')
sections = client.send_get('get_sections/1&suite_id')
cases = client.send_get('get_cases/1&suite_id')

for item in project:
    projectItem = Project(item["id"], item["name"], item["announcement"], item["show_announcement"], item["is_completed"],
    item["completed_on"], item["suite_mode"], item["url"])

    projects.append(projectItem)


print(len(projects))

# print('###################################### SECTIONS ###################################################')
# print(sections)
# print('###################################### CASES ###################################################')
# print(cases)


