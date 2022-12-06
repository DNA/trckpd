import os

class Config():
    DEFAULT_MONGODB_URL = 'mongodb://localhost:27017'

    def __init__(self):
        # export MONGODB_URL="mongodb+srv://<username>:<password>@<url>/<db>?retryWrites=true&w=majority"
        self.mongodb_url = os.environ.get('MONGODB_URL', self.DEFAULT_MONGODB_URL)
