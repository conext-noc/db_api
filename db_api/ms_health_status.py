import os
import boto3
from dotenv import load_dotenv
from botocore.exceptions import NoCredentialsError

load_dotenv()


def get_health_status():
    res = []
    try:
        # Create a session using your AWS access key and secret access key
        session = boto3.Session(
            aws_access_key_id=os.environ["AWS_ACCESS_KEY"],
            aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
        )

        eb_client = session.client("elasticbeanstalk", region_name="us-west-2")

        envs = eb_client.describe_environments()["Environments"]
        
        for env in envs:
            res.append(
                {
                    "name": env["EnvironmentName"],
                    "app-name": env["ApplicationName"],
                    "version": env.get("VersionLabel") or "",
                    "url-eb": env["CNAME"],
                    "status": env["Status"],
                    "health": env["Health"],
                    "health-status": env["HealthStatus"],
                }
            )

        return {"error": False, "message": "success", "data": res}

    except NoCredentialsError:
        return {
            "error": True,
            "message": "Unable to locate AWS credentials.",
            "data": None,
        }


get_health_status()