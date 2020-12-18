class Run:
    def __init__(self, id, name, is_completed, project_id, suite_id, created_by, url):
        self.id = id
        self.name = name
        self.is_completed = is_completed
        self.project_id = project_id
        self.suite_id = suite_id
        self.url = url
        self.created_by = created_by