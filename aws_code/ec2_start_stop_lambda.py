import boto3
import time
import os

INSTANCE_ID = os.environ.get("INSTANCE_ID")

ec2 = boto3.client("ec2")
ssm = boto3.client("ssm")

def wait_for_instance():
    waiter = ec2.get_waiter("instance_running")
    waiter.wait(InstanceIds=[INSTANCE_ID])

def run_command():
    response = ssm.send_command(
        InstanceIds=[INSTANCE_ID],
        DocumentName="AWS-RunShellScript",
        Parameters={
            "commands": [
                "bash /home/ec2-user/nse/run_job.sh"
            ]
        }
    )
    return response["Command"]["CommandId"]

def wait_for_command(command_id):
    while True:
        time.sleep(10)
        output = ssm.list_command_invocations(
            CommandId=command_id,
            Details=True
        )
        if output["CommandInvocations"]:
            status = output["CommandInvocations"][0]["Status"]
            if status in ["Success", "Failed", "Cancelled", "TimedOut"]:
                print("Command finished with status:", status)
                break

def lambda_handler(event, context):
    print("Starting EC2...")
    ec2.start_instances(InstanceIds=[INSTANCE_ID])

    print("Waiting for instance to be running...")
    wait_for_instance()

    print("Running script via SSM...")
    command_id = run_command()

    print("Waiting for script to finish...")
    wait_for_command(command_id)

    print("Stopping EC2...")
    ec2.stop_instances(InstanceIds=[INSTANCE_ID])

    return "Done"