from typing import Any

from aws_cdk import aws_apigateway as _apigw
from aws_cdk import aws_iam as iam
from aws_cdk import aws_lambda as _lambda
from aws_cdk import core as cdk


class LinetwstockCdkStackProd(cdk.Stack):
    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs: Any) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Lambda docker image
        code = _lambda.DockerImageCode.from_image_asset(
            directory="./",
            file="docker/cloud/Dockerfile",
        )

        # Lambda function
        backend = _lambda.DockerImageFunction(
            self,
            id="LinetwstockProd",
            code=code,
            environment={
                "ENV": "PRODUCTION",
            },
            timeout=cdk.Duration.seconds(12),
        )

        # Attach ssm policy to Lambda
        statement = iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=[
                "ssm:GetParameters",
            ],
            resources=[f"arn:aws:ssm:{self.region}:{self.account}:parameter/*"],
        )
        backend.add_to_role_policy(statement=statement)

        # API Gateway
        _apigw.LambdaRestApi(
            self,
            id="linetwstock-prod",
            handler=backend,
            proxy=True,
        )

        cdk.CfnOutput(self, id="Region", value=self.region)
