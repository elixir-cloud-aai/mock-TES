# mock-TES

Connexion-based mock-up service implementing the GA4GH Task Execution Service
API schema. The service was developed to implement and test [TEStribute](https://github.com/elixir-europe/TEStribute),
a task distribution logic package for TES instances. It features an extended
TES specification to provide parameters required for the model underlying the
task distribution logic.

## TES spec modifications

Coming soon...

## Deployment

Full instructions coming soon...

```bash
# Clone repository
git clone git@github.com:elixir-europe/WES-ELIXIR.git
cd mock-TES

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

## Usage

The service is available at the following URL:
<http://localhost:9001/ga4gh/tes/v1/>

> Note that host and port may differ depending on the values specified in:
`mock_tes/config/app_config.yaml`

Explore the service via the Swagger UI:

```bash
firefox http://localhost:9001/ga4gh/tes/v1/ui/
```

Download/access the specs in JSON format:

```bash
wget http://localhost:9001/ga4gh/tes/v1/swagger.json
```