import os
from dotenv import load_dotenv
import boto3
from botocore.exceptions import NoCredentialsError

load_dotenv()


def get_health_status():
    data = {"Ops-env": {}, "Ins-env": {}, "Sch-env": {}, "Mod-env": {}, "Mon-env": {}}
    res = []
    envs = list(data.keys())
    try:
        # Create a session using your AWS access key and secret access key
        session = boto3.Session(
            aws_access_key_id=os.environ["AWS_ACCESS_KEY"],
            aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
        )

        # Create an AWS Elastic Beanstalk client
        eb_client = session.client("elasticbeanstalk", region_name="us-west-2")

        # Get information about the environment
        for environment in envs:
            eb_envs = eb_client.describe_environments(EnvironmentNames=[environment])
            if len(eb_envs["Environments"]) == 0:
                data[environment] = None
            else:
                response = eb_envs["Environments"][0]
                data[environment]["health"] = (
                    response["HealthStatus"]
                    if "HealthStatus" in response
                    else response["Health"]
                )
                data[environment]["application"] = response["ApplicationName"]
                data[environment]["version"] = response["VersionLabel"]
                data[environment]["status"] = response["Status"]
        for environments in data.items():
            res.append(environments[1])

        return {"error": False, "message": "success", "data": res}

    except NoCredentialsError:
        return {
            "error": True,
            "message": "Unable to locate AWS credentials.",
            "data": None,
        }
