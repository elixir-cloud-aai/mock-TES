from datetime import datetime, timezone
from json import decoder, loads
from pymongo.errors import DuplicateKeyError
from services.db import PyMongoUtils

#from services.utils import ServerUtils

class Tasks:
    def __init__(self,collection, index, task_id_length, task_id_charset, default_page_size, debug=False, dummy_request=None, limit=None):

        self.debug = debug

    def __create_task_id(self):
        '''
        create a random task id
        :return: string using the charset defined for id's
        '''
        return None

    def __init_create_document(self):
        """
        initialise a new task
        :return: dict of params defined
        """
        return None

    def __manage_drs_attachments(self):
        """
        should manage the attached drs id's
        :return:
        """

    def __cancel_task(self):
        """

        :return:
        """

    def list_tasks(self):
        """

        :return:
        """

    def tasks_info(self):
        """

        :return:
        """

