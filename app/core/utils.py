import boto3


def get_ssm_parameters(param_names: list[str]) -> dict:
    ssm = boto3.client("ssm")
    ssm_response = ssm.get_parameters(Names=param_names, WithDecryption=True)

    params = {}
    for param in ssm_response["Parameters"]:
        params[param["Name"]] = param["Value"]

    if len(ssm_response["InvalidParameters"]) > 0:
        return {"error": "Invalid Parameter Name"}

    return params
