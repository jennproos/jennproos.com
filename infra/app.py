#!/usr/bin/env python3
from aws_cdk import (
    App,
    Environment
)

from infra.infra_stack import InfraStack

app = App()
env = Environment(account='120086452202', region='us-east-1')

InfraStack(app, "InfraStack", env=env)

app.synth()
