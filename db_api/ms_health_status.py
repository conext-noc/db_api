import os
import boto3
from dotenv import load_dotenv
from botocore.exceptions import NoCredentialsError, NoRegionError

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
                    "health-status": env.get("HealthStatus") or "",
                }
            )

        return {"error": False, "message": "success", "data": res}

    except NoCredentialsError:
        return {
            "error": True,
            "message": "Unable to locate AWS credentials.",
            "data": None,
        }


def get_ms_ips():
    ips = []
    try:
        session = boto3.Session(
            aws_access_key_id=os.environ["AWS_ACCESS_KEY"],
            aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
            region_name="us-west-2",
        )

        eb_client = session.client("elasticbeanstalk")
        ec2_client = session.client("ec2")

        envs = eb_client.describe_environments()["Environments"]

        for env in envs:
            env_name = env["EnvironmentName"]
            response = eb_client.describe_environment_resources(
                EnvironmentName=env["EnvironmentName"]
            )
            instance_ids = [
                resource["Id"]
                for resource in response["EnvironmentResources"]["Instances"]
            ]
            ec2_instances = ec2_client.describe_instances(InstanceIds=instance_ids)

            env_ec2_ip = ec2_instances["Reservations"][0]["Instances"][0][
                "PublicIpAddress"
            ]
            if env_name != "db-api-env":
                ips.append({"name": f"{env_name}-rule", "new_ip_addr": env_ec2_ip})

            # Check if the IP and name match the patterns
        return {
                    "error": False,
                    "message": "success",
                    "data": ips,
                }

    except NoCredentialsError:
        return {
            "error": True,
            "message": "Unable to locate AWS credentials.",
            "data": None,
        }
    except NoRegionError:
        return {
            "error": True,
            "message": "Unable to locate AWS Region Name.",
            "data": None,
        }
    pass