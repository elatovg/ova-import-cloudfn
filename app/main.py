#!/usr/bin/env python3
"""
Simple CloudFn to Import OVA as a machine image
"""
import base64
from google.cloud.devtools import cloudbuild_v1
import google.auth
from datetime import datetime


def import_ova_with_cloudbuild(gcs_path):
    """Create and execute a simple Google Cloud Build configuration,
    print the in-progress status and print the completed status."""

    # Authorize the client with Google defaults
    credentials, project_id = google.auth.default()
    client = cloudbuild_v1.services.cloud_build.CloudBuildClient()

    build = cloudbuild_v1.Build()

    # Add date to image name
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y-%H-%M-%S")
    image = f"Ubuntu_{dt_string}"

    # Create a build using the parameters from
    # https://cloud.google.com/compute/docs/machine-images/import-machine-from-virtual-appliance#api
    build.steps = [{
        "name":
            "gcr.io/compute-image-tools/gce_ovf_import:release",
        "args": [
            f"-machine-image-name={image}", f"-ovf-gcs-path={gcs_path}",
            "-os=ubuntu-2004", "-client-id=api", "-timeout=7000s"
        ]
    }]

    operation = client.create_build(project_id=project_id, build=build)
    # Print the in-progress operation
    print("IN PROGRESS:")
    print(operation.metadata)

    result = operation.result()
    # Print the completed status
    print("RESULT:", result.status)


def main(event, context):
    """ Main Entry point for the cloudfunction"""
    print(
        """This Function was triggered by messageId {} published at {} to {}""".
        format(context.event_id, context.timestamp, context.resource["name"]))

    if 'data' in event:
        print(base64.b64decode(event['data']).decode('utf-8'))
        ova_file = "gs://elatov-demo-keys/ubuntu-20.04-server-cloudimg-amd64.ova"
        import_ova_with_cloudbuild(ova_file)
        # import_ova_with_cloudbuild()
    # else:
    #     action = 'create'
