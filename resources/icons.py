import os

def icon_path(icon_name):
    return os.path.join(os.path.dirname(__file__), 'icon', icon_name)
