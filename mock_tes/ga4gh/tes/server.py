"""
Controler for the GA4GH Task Execution Schema Server
"""
import json
import logging
from random import randint

from addict import Dict
from connexion import request
from flask import current_app
from werkzeug.exceptions import BadRequest


def GetTaskInfo(body):  # noqa: E501
    response = __get_task_info(
        resources=request.json,
        params=current_app.config["task_info"]
    )
    return response


def CancelTask(id):  # noqa: E501
    # Not implemented
    return {}


def CreateTask(body):  # noqa: E501
    # Not implemented
    return {'id': 'task_id'}


def GetServiceInfo():  # noqa: E501
    # Not implemented
    return {}


def GetTask(id, view=None):  # noqa: E501
    # Not implemented
    return {'executors': []}


def ListTasks(name_prefix=None, page_size=None, page_token=None, view=None):  # noqa: E501
    # Not implemented
    return {'tasks': []}


def UpdateTaskInfoConfig(body):  # noqa: E501
    current_app.config["task_info"] = __update_task_info_config(
        config_new=body,
        config_old=current_app.config["task_info"],
    )
    return current_app.config["task_info"]


def __get_task_info(resources, params):
    '''
    Helper function to estimate task queueing time and costs and build the
    response object (tesTaskInfo object).
    '''
    costs_compute = __get_compute_costs(
        resources=resources,
        currency=params['currency'],
        unit_costs_cores=params['unit_costs']['cpu_usage'],
        unit_costs_memory=params['unit_costs']['memory_consumption'],
    )
    costs_storage = __get_storage_costs(
        resources=resources,
        currency=params['currency'],
        unit_costs_storage=params['unit_costs']['data_storage']
    )
    time_queue = __get_queue_time()
    return {
        'estimated_compute_costs': costs_compute,
        'estimated_queue_time_sec': time_queue,
        'estimated_storage_costs': costs_storage,
        'unit_costs_data_transfer': {
		    'amount': params['unit_costs']['data_transfer'],
		    'currency': params['currency'],
	    },
    }


def __get_compute_costs(
    resources,
    currency='BTC',
    unit_costs_cores=0,
    unit_costs_memory=0,
):
    '''
    Helper function to estimate task costs from tesResources object. Returns a
    dictionary of tesCosts objects.
    '''
    # Get execution time
    t = resources['execution_time_sec']

    # Calculate partial compute costs
    c_cores = t * resources['cpu_cores'] * unit_costs_cores
    c_mem = t * resources['ram_gb'] * unit_costs_memory

    # Calculate total compute costs
    c_total = c_cores + c_mem

    # Return dictionary of tesCosts objects
    return {
        'amount': c_total,
        'currency': currency,
    }


def __get_storage_costs(
    resources,
    currency='BTC',
    unit_costs_storage=0,
):
    '''
    Helper function to estimate task storage costs from tesResources object.
    Returns a tesCosts object.
    '''
    return {
        'amount': resources['disk_gb'] * unit_costs_storage,
        'currency': currency,
    }

def __get_queue_time():
    '''
    Helper function to estimate task queue time from tesResources object.
    Returns a random float.
    '''
    return float(randint(0, 3600))


def __update_task_info_config(config_new, config_old):
    '''
    Helper function that updates the task info configuration given the old and
    new config.
    '''
    if __hasExtraKeys(config_new, config_old):
        raise BadRequest
    else:
        config_old = Dict(config_old)
        config_old.update(config_new)
        return config_old


def __hasExtraKeys(query, ref):
    '''
    Helper function that returns `True` if dictionary `query` contains keys
    that dictionary `ref` does not contain. Works recursively.
    '''
    for key in query:
       if key not in ref:
           return True
       elif isinstance(query[key], dict):
           return __hasExtraKeys(query[key], ref[key])
    return False
