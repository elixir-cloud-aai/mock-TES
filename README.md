# mock-TES

[Connexion]-based mockup service implementing parts of the GA4GH [Task Execution
Service] (TES) API schema. The service was developed to implement and test
[TEStribute], a task distribution logic package for TES instances. It features
an extended TES specification to provide parameters required for the model
underlying the task distribution logic.

## Usage

Once deployed and started ([see below](#Deployment)), the service will be
available at:  
<http://localhost:9001/ga4gh/tes/v1/>

You can explore the service via the Swagger UI:

```bash
firefox http://localhost:9001/ga4gh/tes/v1/ui/
```

The specifications, in JSON format, can be retrieved with:

```bash
wget http://localhost:9001/ga4gh/tes/v1/swagger.json
```

> Note that host and port can be set manually in the [config] file. In that
> case, the values in the URLs above need to be replaced as well.

The client [TES-cli] can be used to send requests to the service.

## Deployment

`mock-TES` can be deployed via containers (preferred) or after manual
installation of all dependencies.

In both cases, the repository first needs to be cloned with:

```bash
git clone git@github.com:elixir-europe/mock-TES.git
```

Afterwards traverse to the repository's root directory:

```bash
cd mock-TES
```

### Containerized deployment

> "Production-like" containerized deployment without HTTP server/load balancer
> etc.

#### Requirements (Dockerized deployment)

* [Git] (tested with version 2.17.1)
* [Docker] (tested with version 18.09.6)
* [docker-compose] (tested with version 1.24.0)

#### Building & starting the service

```bash
# Build application image
# [NOTE] Image re-building is not always necessary. Inspect the `Dockerfile`
#        to check which changes will need re-building.
docker-compose build
# Start service
docker-compose up -d
```

#### Other useful commands

```bash
# Check logs
docker-compose logs
# Shut down service
docker-compose down
```

### Non-containerized deployment

> Deployment for local development without containers, HTTP server/load
> balancer etc.

#### Requirements

* [Git] (tested with version 2.17.1)
* [Python] (tested with versions 2.7.15+ & 3.6.8)
* [pip] (tested with version 19.1.1)
* [virtualenv] (tested with version 15.1.0)

#### Installing & starting the service

```bash
# Set up Python virtual environment
virtualenv -p `which python3` venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install app
python setup.py develop

# Run service
python mock_tes/Server.py
```

## Implementation details

Note that only those parts of the service are implemented that are required for
developing, testing and debugging [TEStribute]. For all other endpoints only
stubs are implemented that return the most basic valid response (typically an
"empty" JSON object).

### Modifications to TES specs

An endpoint `/tasks/task-info` was added to commit [`d55bf88`] of the [Task
Execution Service] [OpenAPI] specification. It provides parameters required for
[TEStribute]'s task distribution logic.

The [modified specifications] as well as a snapshot of the [unmodified
specifications] are available in this repository.

This section outlines the definitions of the endpoint and underlying request
and response models.

#### Endpoint `/tasks/task-info`

The endpoint `/tasks/task-info` returns estimations of queue time and incurred
costs if a task with a given set of resource requirements were to be computed
on this TES instance right now. Within the framework of [TEStribute], these
parameters allow informed decisions with regards to which of a number of TES
instances a given task should be sent to. The endpoint is defined by:

```yaml
/tasks/task-info:
    post:
      summary: |-
        Provides estimates for the queue time and incurred costs for a task
        with the given resource requirements.
      operationId: GetTaskInfo
      responses:
        '200':
          description: ''
          schema:
            $ref: '#/definitions/tesTaskInfo'
      parameters:
        - name: body
          in: body
          required: true
          schema:
            $ref: '#/definitions/tesResources'
      tags:
        - TaskService
      x-swagger-router-controller: ga4gh.tes.server
```

#### Request model `tesResources`

A property `execution_time_min` was added to the model describing a task's
resource requirements. The entire model is now defined as follows:

```yaml
 tesResources:
    type: object
    properties:
      execution_time_min:
        type: integer
        format: int64
        description: Requested execution in minutes (min)
      cpu_cores:
        type: integer
        format: int64
        description: Requested number of CPUs
      preemptible:
        type: boolean
        format: boolean
        description: Is the task allowed to run on preemptible compute instances (e.g. AWS Spot)?
      ram_gb:
        type: number
        format: double
        description: Requested RAM required in gigabytes (GB)
      disk_gb:
        type: number
        format: double
        description: Requested disk size in gigabytes (GB)
      zones:
        type: array
        items:
          type: string
        description: Request that the task be run in these compute zones.
    description: Resources describes the resources requested by a task.
```

#### Response model `tesTaskInfo`

A valid request to the endpoint results in a response defined in the following
model:

```yaml
  tesTaskInfo:
    type: object
    properties:
      costs_total:
        $ref: '#/definitions/tesCosts'
        description: |-
          Estimated total incurred costs for running a task with the given
          resource requirements on this TES instance.
      costs_cpu_usage:
        $ref: '#/definitions/tesCosts'
        description: |-
          Estimated incurred costs for CPU use.
      costs_memory_consumption:
        $ref: '#/definitions/tesCosts'
        description: |-
          Estimated incurred costs for memory consumption.
      costs_data_storage:
        $ref: '#/definitions/tesCosts'
        description: |-
          Estimated incurred costs for storage use.
      costs_data_transfer:
        $ref: '#/definitions/tesCosts'
        description: |-
          Unit costs for transferring 1 GB of data across 1000 km.
      queue_time:
        $ref: '#/definitions/tesDuration'
        description: |-
          Given the current load on this TES instance, returns an estimate of
          the time that a task with the given resource requirements will spend
          in the task queue.
    description: |-
      Given a set of resource requirements, returns the estimated queue time
      and total incurred costs. Allows informed decisions with regard to which
      TES instance a given task should be sent to.
```

The response model relies on additional models `tesCosts` and `tesDuration`
which are described as follows:

##### `tesCosts`

```yaml
  tesCosts:
    type: object
    properties:
      amount:
        type: number
        format: double
        description: Numeric value specifying an amount of money.
      currency:
        type: string
        enum:
          - ARBITRARY
          - BTC
          - EUR
          - USD
        description: Currency/unit of the costs.
    description: Generic object specifying an amount of money.
```

##### `tesDuration`

```yaml
  tesDuration:
    type: object
    properties:
      duration:
        type: integer
        format: int64
        description: Integer value specifying a length of time.
      unit:
        type: string
        enum:
          - SECONDS
          - MINUTES
          - HOURS
        description: Unit of the duration.
    description: Generic object specifying a length of time.
```

### Service configuration

The service can be configured with different unit costs for CPU and memory
usage, data transfer and storage. Default values for the corresponding
parameters are listed in `task_info` section of the service's [config] and they
can be edited by the user before starting the service.

Alternatively (and preferably), these parameters can be modified in the running
service via the `/update-config` endpoint, which is particularly useful for
setting up environments for various testing scenarios for [TEStribute]. The
endpoint is defined in the [config specifications]:

```yaml
  /update-config:
    post:
      summary: Update task info config
      operationId: UpdateTaskInfoConfig
      responses:
        '200':
          description: ''
          schema:
            $ref: '#/definitions/tesTaskInfoConfig'
      parameters:
        - name: body
          in: body
          schema:
            $ref: '#/definitions/tesTaskInfoConfig'
          required: true
          description: ''
      tags:
        - TaskService
      x-swagger-router-controller: ga4gh.tes.server
```

It relies on the following models:

```yaml
  tesTaskInfoConfig:
    type: object
    properties:
      currency:
        type: string
        enum:
          - ARBITRARY
          - BTC
          - EUR
          - USD
        description: Currency/unit of the costs.
      time_unit:
        type: string
        enum:
          - SECONDS
          - MINUTES
          - HOURS
        description: Unit of the queue time.
      unit_costs:
        $ref: '#/definitions/tesTaskInfoCosts'
  tesTaskInfoCosts:
    type: object
    properties:
      cpu_usage:
        type: integer
        format: int64
        description: costs per core
      memory_consumption:
        type: integer
        format: int64
        description: costs of computation per GB
      data_storage:
        type: integer
        format: int64
        description:  cost of data storage  GB
      data_transfer:
        type: integer
        format: int64
        description: cost of data transfer per GB and 1000 km
```

[TES-cli] can be used to update the task info parameters.

> Note that while the `/update-config` endpoint can be accessed via the same
> root URI (and explored via the Swagger UI), it was not included in the
> [modified TES specifications], but rather added to it _on the fly_ when the
> service is started.

## Contributing

This project is a community effort and lives off your contributions, be it in
the form of bug reports, feature requests, discussions, or fixes and other code
changes. Please read the [contributing guidelines] if you want to contribute.
And please mind the [code of conduct] for all interactions with the community.

## Versioning

Development of the app is currently still in alpha stage, and current versioning
is for internal use only. In the future, we are aiming to adopt [semantic
versioning] that is synchronized to the versioning of [TEStribute] and
[TES-cli] in order to ensure that these apps will be compatible as long as both
their major and minor versions match.

## License

This project is covered by the [Apache License 2.0] also available [shippied
with this repository](LICENSE).

## Contact

Please contact the [project leader](mailto:alexander.kanitz@sib.swiss) for
inquiries, proposals, questions etc. that are not covered by the
[Contributing](#Contributing) section.

## Acknowledgments

The project is a collaborative effort under the umbrella of the [ELIXIR Cloud
and AAI] group. It was started during the [2019 Google Summer of Code] as part
of the [Global Alliance for Genomics and Health] [organization].

![logo banner]

[2019 Google Summer of Code]: <https://summerofcode.withgoogle.com/projects/#6613336345542656>
[Apache License 2.0]: <https://www.apache.org/licenses/LICENSE-2.0>
[code of conduct]: CODE_OF_CONDUCT.md
[config]: mock_tes/config/app_config.yaml
[config_specs]: mock_tes/specs/schema.task_execution_service.config_update.openapi.yaml
[Connexion]: <https://github.com/zalando/connexion>
[contributing guidelines]: CONTRIBUTING.md
[`d55bf88`]: <https://github.com/ga4gh/task-execution-schemas/tree/d55bf880062442288afc95665aa0e21fbba77b20>
[Docker]: <https://docs.docker.com/install/>
[docker-compose]: <https://docs.docker.com/compose/install/>
[ELIXIR Cloud and AAI]: <https://elixir-europe.github.io/cloud/>
[Git]: <https://git-scm.com/book/en/v2/Getting-Started-Installing-Git>
[Global Alliance for Genomics and Health]: <https://www.ga4gh.org/>
[logo banner]: logos/logo-banner.svg
[modified specifications]: mock_tes/specs/schema.task_execution_service.d55bf88.openapi.modified.yaml
[modified TES specifications]: mock_tes/specs/schema.task_execution_service.d55bf88.openapi.modified.yaml
[OpenAPI]: <https://swagger.io/specification/>
[organization]: <https://summerofcode.withgoogle.com/organizations/6643588285333504/>
[pip]: <https://pip.pypa.io/en/stable/installing/>
[Python]: <https://www.python.org/downloads/>
[semantic versioning]: <https://semver.org/>
[Task Execution Service]: <https://github.com/ga4gh/task-execution-schemas>
[TES-cli]: <https://github.com/ga4gh/task-execution-schemas>
[TEStribute]: <https://github.com/elixir-europe/TEStribute>
[unmodified specifications]: mock_tes/specs/schema.task_execution_service.d55bf88.openapi.yaml
[virtualenv]: <https://virtualenv.pypa.io/en/stable/installation/>
