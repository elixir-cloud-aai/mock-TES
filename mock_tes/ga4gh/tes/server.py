"""
Controler for the GA4GH Task Execution Schema Server
"""
from flask import current_app
from pymongo import MongoClient
from copy import deepcopy

def CancelTask(id):  # noqa: E501
    # to-do handle errors
    return None


def CreateTask(body):  # noqa: E501
    # to-do handle errors
    return {200: "a test"}


def GetServiceInfo():  # noqa: E501
    # to-do handle errors
    return None


def GetServiceInfoTaskInfo():  # noqa: E501
    tasks_info = deepcopy(current_app.config['service_info']['tasks_info'])
    return {200: [tasks_info]}


def GetTask(id, view=None):  # noqa: E501
    # to-do handle errors
    return None


def ListTasks(
    name_prefix=None, page_size=None, page_token=None, view=None
):  # noqa: E501
    # to-do handle errors
    return None


# to-do add logger
def log_request(request, response):
    """Writes request and response to log."""
    # to-do: write decorator for request logging
