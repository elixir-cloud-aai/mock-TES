from datetime import datetime, timezone
from json import decoder, loads
from pymongo.errors import DuplicateKeyError
from services.db import PyMongoUtils

#from services.utils import ServerUtils

class Tasks:
    def __init__(self,collection, index, task_id_length, task_id_charset, default_page_size, debug=False, dummy_request=None, limit=None):

        self.debug = debug

        self.collection = collection
        self.index = index

        self.task_id_length = task_id_length
        self.task_id_charset = task_id_charset

        self.default_page_size = default_page_size

        self.latest_object_id = PyMongoUtils.find_id_latest(self.collection)

    def __create_task_id(self):
        '''
        create a random task id
        :return: string using the charset defined for id's
        '''
        return None

    def __init_create_document(self, task_id, state, name, description, inputes, resources, executors, volumes, tags, logs):
        """
        initialise a new task
        :return: dict of params defined
        """
        document = Dict()

        # add as keys

        return None

    def __manage_tes_inputs(self):
        """
        should manage the attached drs id's
        :return:
        """

    def __cancel_task(self):
        """

        :return:
        """

    def __manage_tes_resources(self):
        """

        :return:
        """

    def tasks_info(self):
        """

        :return:
        """
