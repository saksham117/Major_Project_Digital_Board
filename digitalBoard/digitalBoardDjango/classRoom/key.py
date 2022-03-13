import os

def returnKey():
    key = os.environ.get('OPEN_AI_KEY')
    return key
