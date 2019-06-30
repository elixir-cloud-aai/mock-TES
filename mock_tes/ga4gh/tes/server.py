"""
Controler for the GA4GH Task Execution Schema Server
"""
from flask import current_app
from copy import deepcopy


def CancelTask(id):  # noqa: E501
    # to-do return some value
    return None


def CreateTask(body):  # noqa: E501
    # to-do return some value
    return {200: "a test"}


def GetServiceInfo():  # noqa: E501
    # to-do return some value
    return None


def GetServiceInfoTaskInfo(body):  # noqa: E501
    # to-do :
    #       add a function to update the config file for mean rate of task arrival &
    #       mean rate of requests arrival per system
    #       use updated mean rate of task arrival for generation of random server load

    # to-do: add function :
    #       1. calculation of t queue
    #       2. calculation of t exec
    #       3. calculation of DRS instance's t data transfer
    # copy the service-info/task-info parameters
    tasks_info = deepcopy(current_app.config["service_info"]["tasks_info"])

    print(tasks_info)
    # to-do :
    #       add formula to approximate the cost

    # to-do :
    #       return approximate cost

    # returns config values
    return {200: [tasks_info]}


def GetTask(id, view=None):  # noqa: E501
    # to-do return some value
    return None


def ListTasks(
    name_prefix=None, page_size=None, page_token=None, view=None
):  # noqa: E501
    # to-do return some value
    return None


# to-do add logger
def log_request(request, response):
    """Writes request and response to log."""
    # to-do: write decorator for request logging
