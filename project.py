class Project:
    def __init__(self, id, name, announcement, show_announcement, is_completed, completed_on, suite_mode, url):
        self.id = id
        self.name = name
        self.announcement = announcement
        self.show_announcement = show_announcement
        self.is_completed = is_completed
        self.completed_on = completed_on
        self.suite_mode = suite_mode
        self.url = url