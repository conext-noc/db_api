# from django.test import TestCase

# Create your tests here.
import os
import re
import unittest
import boto3
from botocore.exceptions import NoCredentialsError, NoRegionError


class TestAWSConn(unittest.TestCase):
    def test_aws_connection(self):
        try:
            session = boto3.Session(
                aws_access_key_id=os.environ["AWS_ACCESS_KEY"],
                aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
                region_name="us-west-2",
            )
            eb_client = session.client("elasticbeanstalk", region_name="us-west-2")
            eb_data = eb_client.describe_environments()

            self.assertTrue("Environments" in eb_data)
            if "Environments" in eb_data:
                print("✅ -> connection to AWS successful")
        except NoCredentialsError:
            self.fail("Unable to locate AWS credentials. Check your configuration.")
        except NoRegionError:
            self.fail("No AWS region provided.")
        except Exception as e:
            self.fail(f"AWS connection test failed with error: {str(e)}")

    def test_aws_ip_getter(self):
        ipv4_pattern = r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"
        env_name_pattern = r"^[a-zA-Z0-9_-]+$"

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

                # Check if the IP and name match the patterns
                self.assertTrue(
                    re.match(ipv4_pattern, env_ec2_ip), f"Invalid IP: {env_ec2_ip}"
                )
                self.assertTrue(
                    re.match(env_name_pattern, env_name), f"Invalid name: {env_name}"
                )

                if re.match(ipv4_pattern, env_ec2_ip) and re.match(
                    env_name_pattern, env_name
                ):
                    print(
                        f"✅ -> valid IP: {env_ec2_ip:^15} and valid name: {env_name:^7}"
                    )

        except NoCredentialsError:
            self.fail("No AWS credentials provided.")
        except NoRegionError:
            self.fail("No AWS region provided.")
