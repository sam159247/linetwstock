import os

from aws_cdk import core as cdk

from app.cdk_stack.prod.linetwstock_stack import LinetwstockCdkStackProd
from app.cdk_stack.stg1.linetwstock_stack import LinetwstockCdkStackStg1

app = cdk.App()
ACCOUNT = app.node.try_get_context("account") or os.environ.get("CDK_DEFAULT_ACCOUNT", "unknown")
REGION = app.node.try_get_context("region") or os.environ.get("CDK_DEFAULT_REGION", "unknown")
env = cdk.Environment(region=REGION, account=ACCOUNT)

# Staging_1 environment
LinetwstockCdkStackStg1(
    app,
    "linetwstock-cdk-stack-stg1",
    env=env,
)

# Production environment
LinetwstockCdkStackProd(
    app,
    "linetwstock-cdk-stack-prod",
    env=env,
)

app.synth()
