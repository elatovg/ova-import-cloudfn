#!/usr/bin/env python3
"""
Simple CloudFn to Import OVA as a machine image
"""
from datetime import datetime
from google.cloud.devtools import cloudbuild_v1
import google.auth
from google.protobuf.duration_pb2 import Duration


def import_ova_with_cloudbuild(gcs_path):
    """Create and execute a simple Google Cloud Build configuration,
    print the in-progress status and print the completed status."""

    # Authorize the client with Google defaults
    _credentials, project_id = google.auth.default()
    client = cloudbuild_v1.services.cloud_build.CloudBuildClient()

    build = cloudbuild_v1.Build()

    # Add date to image name
    now = datetime.now()
    dt_string = now.strftime("%m_%d_%Y_%H_%M_%S")
    image = f"ubuntu-{dt_string}"

    # Create a build using the parameters from
    # https://cloud.google.com/compute/docs/machine-images/import-machine-from-virtual-appliance#api
    build.steps = [{
        "name":
            # "gcr.io/compute-image-tools/gce_ovf_import:release",
            "gcr.io/compute-image-tools/gce_vm_image_import:release",
        "args": [
            # f"-machine-image-name={image}", f"-ovf-gcs-path={gcs_path}",
            # "-os=ubuntu-2004", "-client-id=api", "-timeout=7000s",
            f"-image_name={image}", f"-source_file={gcs_path}",
            "-os=ubuntu-2004", "-client_id=api", "-timeout=7000s"
        ],
    }]
    build.timeout = Duration(seconds=2400)
    build.tags = [image]
    print(image)
    print(build.tags)
    operation = client.create_build(project_id=project_id, build=build)
    # Print the in-progress operation
    print("IN PROGRESS:")
    print(operation.metadata)

    # result = operation.result()
    # # Print the completed status
    # print("RESULT:", result.status)


def main(event, context):
    """ Main Entry point for the cloudfunction"""
    print(
        """This Function was triggered by messageId {} published at {} to {}""".
        format(context.event_id, context.timestamp, context.resource["name"]))

    # print(event)
    if 'bucket' in event:
        bucket_name = event["bucket"]
        filename = event["name"]
        ova_file = f"gs://{bucket_name}/{filename}"
        import_ova_with_cloudbuild(ova_file)
