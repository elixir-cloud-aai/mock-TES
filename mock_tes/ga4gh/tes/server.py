"""
Controler for the GA4GH Task Execution Schema Server
"""
import json
import logging
from random import randint

from connexion import request
from flask import current_app


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


def __get_task_info(resources, params):
    '''
    Helper function to estimate task queueing time and costs and build the
    response object (tesTaskInfo object).
    '''
    costs = __get_compute_costs(
        resources=resources,
        currency=params['currency'],
        unit_costs_cores=params['unit_costs']['cpu_usage'],
        unit_costs_memory=params['unit_costs']['memory_consumption'],
        unit_costs_storage=params['unit_costs']['data_storage']
    )
    queue_time = __get_queue_time(
        resources=resources,
        time_unit=params['time_unit']
    )
    return {
        'costs_total': costs['total'],
        'costs_cpu_usage': costs['cpu_usage'],
        'costs_memory_consumption': costs['memory_consumption'],
        'costs_data_storage': costs['data_storage'],
        'costs_data_transfer': {
		'amount': params['unit_costs']['data_transfer'],
		'currency': params['currency']
	},
        'queue_time': queue_time
    }


def __get_compute_costs(
    resources,
    currency='ARBITRARY',
    unit_costs_cores=0,
    unit_costs_memory=0,
    unit_costs_storage=0
):
    '''
    Helper function to estimate task costs from tesResources object. Returns a
    dictionary of tesCosts objects.
    '''
    # Parse resources
    t = resources['execution_time_min']
    cores = resources['cpu_cores']
    mem = resources['ram_gb']
    size = resources['disk_gb']

    # Calculate partial costs
    c_cores = t * cores * unit_costs_cores
    c_mem = t * mem * unit_costs_memory
    c_storage = t * size * unit_costs_storage

    # Calculate total costs
    c_total = c_cores + c_mem + c_storage

    # Return dictionary of tesCosts objects
    return {
        'total': {
            'amount': c_total,
            'currency': currency
        },
        'cpu_usage': {
            'amount': c_cores,
            'currency': currency
        },
        'memory_consumption': {
            'amount': c_mem,
            'currency': currency
        },
        'data_storage': {
            'amount': c_storage,
            'currency': currency
        }
    }


def __get_queue_time(resources, time_unit):
    '''
    Helper function to estimate task queue time from tesResources object.
    Returns a tesDuration object.
    '''
    duration = randint(0, 3600)
    unit = time_unit
    return {
        'duration': duration,
        'unit': unit
    }
