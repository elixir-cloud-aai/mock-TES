"""
Mock service for the GA4GH Task Execution Schema.
"""
import os
import sys

from connexion import App
from specsynthase.specbuilder import SpecBuilder

from mock_tes.config.app_config import parse_app_config


# Instantiate app object
app = App(
    __name__,
    options={"swagger_ui": True,
             "swagger_json": True},
)

# Parse config
config = parse_app_config(config_var="TES_CONFIG")


def configure_app(app):
    """Configure app"""

    # Add settings
    app = add_settings(app)

    # Add OpenAPIs
    app = add_openapi(app)

    # Add user configuration to Flask app config
    app.app.config.update(config)

    return app


def add_settings(app):
    """Add settings to Flask app instance"""
    try:
        app.host = config["server"]["host"]
        app.port = config["server"]["port"]
        app.debug = config["server"]["debug"]
    except KeyError:
        sys.exit("Config file corrupt. Execution aborted.")

    return app


def add_openapi(app):
    """Add OpenAPI specification to connexion app instance"""
    try:
        specs = SpecBuilder()\
                .add_spec(config["openapi"]["tes"])\
                .add_spec(config["openapi"]["cost_update"])
        app.add_api(
            specs,
            validate_responses=True,
            strict_validation=True,
        )
    except KeyError:
        sys.exit("Config file corrupt. Execution aborted.")

    return app


def main(app):
    """Initialize, configure and run server"""
    app = configure_app(app)
    app.run()


if __name__ == "__main__":
    main(app)
