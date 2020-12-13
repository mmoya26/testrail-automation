from testrail import *
 
client = APIClient('https://mmoya26.testrail.io/')
client.user = 'mmoya18@icloud.com'
client.password = 'password123'

project = client.send_get('get_projects')
sections = client.send_get('get_sections/1&suite_id')
cases = client.send_get('get_cases/1&suite_id')
print('###################################### PROJECTS ###################################################')
print(project)
print('###################################### SECTIONS ###################################################')
print(sections)
print('###################################### CASES ###################################################')
print(cases)


