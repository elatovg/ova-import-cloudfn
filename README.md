# ova-import-cloudfn

## Configure Prereqs
```
gcloud services enable cloudbuild.googleapis.com
```

Mirror Github repo to Cloud Source Repositories (All the instructions are laid out in [Mirroring a GitHub repository](https://cloud.google.com/source-repositories/docs/mirroring-a-github-repository))

Follow instructions from [Prerequisites for importing and exporting VM images](https://cloud.google.com/compute/docs/import/requirements-export-import-images#gcloud_1), configure the necessary permissions to the cloud build and compute service accounts:

```bash
export PROJECT_ID=$(gcloud config list --format 'value(core.project)')
export PROJECT_NUM=$(gcloud projects list --filter="project_id:${PROJECT_ID}"  --format='value(project_number)')
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
   --member "serviceAccount:${PROJECT_NUM}@cloudbuild.gserviceaccount.com" \
   --role 'roles/compute.admin'
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
   --member "serviceAccount:${PROJECT_NUM}@cloudbuild.gserviceaccount.com" \
   --role='roles/iam.serviceAccountUser'
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
   --member "serviceAccount:${PROJECT_NUM}@cloudbuild.gserviceaccount.com" \
   --role='roles/iam.serviceAccountTokenCreator'
```

And now the compute service account:

```bash
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
  --member "serviceAccount:${PROJECT_NUM}-compute@developer.gserviceaccount.com" \
  --role 'roles/compute.storageAdmin'
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
  --member "serviceAccount:${PROJECT_NUM}-compute@developer.gserviceaccount.com" \
  --role 'roles/storage.objectViewer'
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
  --member "serviceAccount:${PROJECT_NUM}-compute@developer.gserviceaccount.com" \
  --role 'roles/storage.objectAdmin'
```
## Create the function
The function will be triggered by an upload to a storage bucket:

```bash
export PROJECT_ID=$(gcloud config list --format 'value(core.project)')
export REGION="us-central1"
export GCS_BUCKET="YOUR_BUCKET"
export CLOUD_SOURCE_REPO="github_elatovg_ova-import-cloudfn"
export SRC_PATH="https://source.developers.google.com/projects/${PROJECT_ID}/repos/${CLOUD_SOURCE_REPO}/moveable-aliases/main/paths/app"
export CLOUD_FN_NAME="build_ova"
gcloud functions deploy ${CLOUD_FN_NAME} --runtime python39 \
  --set-env-vars "PROJECT_ID=${PROJECT_ID}" \
  --trigger-bucket ${GCS_BUCKET} --entry-point main --region ${REGION} \
  --source ${SRC_PATH}
```

## Check the progress
After uploading an ova to your bucket:

```bash
export GCS_BUCKET="YOUR_BUCKET"
> gsutil cp ubuntu-20.04-server-cloudimg-amd64.ova gs://${GCS_BUCKET}/

Copying file://ubuntu-20.04-server-cloudimg-amd64.ova [Content-Type=application/octet-stream]...

- [1 files][520.4 MiB/520.4 MiB]   24.4 MiB/s
Operation completed over 1 objects/520.4 MiB.
```

You can check out the build job and it should be in progress:

```bash
> gcloud builds list --limit 1
ID                                    CREATE_TIME                DURATION  SOURCE  IMAGES  STATUS
fc52df79-c2b6-4733-86e4-d071b2aac4a4  2021-09-17T19:07:55+00:00  3M1S      -       -       WORKING
```

After it's done, you can check out the logs:

```bash
gcloud builds log $(gcloud builds list --limit 1 --format "value(id)")
> gcloud builds log $(gcloud builds list --limit 1 --format "value(id)")
----------------------------- REMOTE BUILD OUTPUT ------------------------------
starting build "fc52df79-c2b6-4733-86e4-d071b2aac4a4"

FETCHSOURCE
BUILD
Pulling image: gcr.io/compute-image-tools/gce_ovf_import:release
release: Pulling from compute-image-tools/gce_ovf_import
9019ec94453e: Already exists
de0a67c50206: Pulling fs layer
f37f46d04c81: Pulling fs layer
ab33b63872f6: Pulling fs layer
ea283727d5ab: Pulling fs layer
5fa82b40c22e: Pulling fs layer
ece82e2b386d: Pulling fs layer
3578d46f0912: Pulling fs layer
af7cda6c2378: Pulling fs layer
5fa82b40c22e: Waiting
ece82e2b386d: Waiting
ea283727d5ab: Waiting
3578d46f0912: Waiting
af7cda6c2378: Waiting
f37f46d04c81: Verifying Checksum
f37f46d04c81: Download complete
ab33b63872f6: Download complete
ea283727d5ab: Verifying Checksum
ea283727d5ab: Download complete
5fa82b40c22e: Verifying Checksum
5fa82b40c22e: Download complete
ece82e2b386d: Verifying Checksum
ece82e2b386d: Download complete
3578d46f0912: Verifying Checksum
3578d46f0912: Download complete
af7cda6c2378: Verifying Checksum
af7cda6c2378: Download complete
de0a67c50206: Verifying Checksum
de0a67c50206: Download complete
de0a67c50206: Pull complete
f37f46d04c81: Pull complete
ab33b63872f6: Pull complete
ea283727d5ab: Pull complete
5fa82b40c22e: Pull complete
ece82e2b386d: Pull complete
3578d46f0912: Pull complete
af7cda6c2378: Pull complete
Digest: sha256:e9bd94f7dbc5c3377ac386c78d2e9778a726fb60641029d3aeb55b53b24530dc
Status: Downloaded newer image for gcr.io/compute-image-tools/gce_ovf_import:release
gcr.io/compute-image-tools/gce_ovf_import:release
[import-ovf]: 2021-09-17T19:08:04Z Starting OVF import workflow.
[import-ovf]: 2021-09-17T19:08:05Z Creating scratch bucket `GCP_PROJECT-ovf-import-bkt-us-central1` in us-central1 region
[import-ovf]: 2021-09-17T19:08:05Z Extracting gs://GCS_BUCKET/ubuntu-20.04-server-cloudimg-amd64.ova OVA archive to gs://GCP_PROJECT-ovf-import-bkt-us-central1/st3wt/ovf
[import-ovf]: 2021-09-17T19:08:05Z Extracting: ubuntu-focal-20.04-cloudimg.ovf to gs://GCP_PROJECT-ovf-import-bkt-us-central1/st3wt/ovf/ubuntu-focal-20.04-cloudimg.ovf
[import-ovf]: 2021-09-17T19:08:05Z Extracting: ubuntu-focal-20.04-cloudimg.mf to gs://GCP_PROJECT-ovf-import-bkt-us-central1/st3wt/ovf/ubuntu-focal-20.04-cloudimg.mf
[import-ovf]: 2021-09-17T19:08:05Z Extracting: ubuntu-focal-20.04-cloudimg.vmdk to gs://GCP_PROJECT-ovf-import-bkt-us-central1/st3wt/ovf/ubuntu-focal-20.04-cloudimg.vmdk
[import-ovf]: 2021-09-17T19:08:15Z Found gs://GCP_PROJECT-ovf-import-bkt-us-central1/st3wt/ovf/ubuntu-focal-20.04-cloudimg.ovf
[import-ovf]: 2021-09-17T19:08:16Z Found gs://GCP_PROJECT-ovf-import-bkt-us-central1/st3wt/ovf/ubuntu-focal-20.04-cloudimg.vmdk
[debug]: 2021-09-17T19:08:16Z Didn't find valid osID in descriptor. Error="cannot determine OS from OVF descriptor. Use --os flag to specify OS. Potential valid values for given osType attribute are: ubuntu-1404, ubuntu-1604, ubuntu-1804"
[debug]: 2021-09-17T19:08:16Z osID candidates: from-user="ubuntu-2004", ovf-descriptor=""
[import-ovf]: 2021-09-17T19:08:16Z Will create instance of `e2-micro` machine type.
[import-disk-1]: 2021-09-17T19:08:19Z Creating Google Compute Engine disk from gs://GCP_PROJECT-demo-ovf-import-bkt-us-central1/st3wt/ovf/ubuntu-focal-20.04-cloudimg.vmdk
[disk-1-inflate]: 2021-09-17T19:08:20Z Validating workflow
[disk-1-inflate]: 2021-09-17T19:08:20Z Validating step "setup-disks"
[disk-1-inflate]: 2021-09-17T19:08:20Z Validating step "import-virtual-disk"
[disk-1-inflate]: 2021-09-17T19:08:21Z Validating step "wait-for-signal"
[disk-1-inflate]: 2021-09-17T19:08:21Z Validating step "cleanup"
[disk-1-inflate]: 2021-09-17T19:08:21Z Validation Complete
[disk-1-inflate]: 2021-09-17T19:08:21Z Workflow Project: GCP_PROJECT
[disk-1-inflate]: 2021-09-17T19:08:21Z Workflow Zone: us-central1-f
[disk-1-inflate]: 2021-09-17T19:08:21Z Workflow GCSPath: gs://GCP_PROJECT-ovf-import-bkt-us-central1/st3wt/ovf-st3wt-1
[disk-1-inflate]: 2021-09-17T19:08:21Z Daisy scratch path: https://console.cloud.google.com/storage/browser/GCP_PROJECT-ovf-import-bkt-us-central1/st3wt/ovf-st3wt-1/daisy-disk-1-inflate-20210917-19:08:20-mtq9n
[disk-1-inflate]: 2021-09-17T19:08:21Z Uploading sources
[disk-1-inflate]: 2021-09-17T19:08:21Z Running workflow
[disk-1-inflate]: 2021-09-17T19:08:21Z Running step "setup-disks" (CreateDisks)
[disk-1-inflate.setup-disks]: 2021-09-17T19:08:21Z CreateDisks: Creating disk "disk-ovf-st3wt-1".
[disk-1-inflate.setup-disks]: 2021-09-17T19:08:21Z CreateDisks: Creating disk "disk-importer-disk-1-inflate-mtq9n".
[disk-1-inflate.setup-disks]: 2021-09-17T19:08:21Z CreateDisks: Creating disk "disk-disk-1-inflate-scratch-mtq9n".
[disk-1-inflate]: 2021-09-17T19:08:33Z Step "setup-disks" (CreateDisks) successfully finished.
[disk-1-inflate]: 2021-09-17T19:08:33Z Running step "import-virtual-disk" (CreateInstances)
[disk-1-inflate.import-virtual-disk]: 2021-09-17T19:08:33Z CreateInstances: Creating instance "inst-importer-disk-1-inflate-mtq9n".
[debug]: 2021-09-17T19:08:40Z Started checksum calculation.
[shadow-disk-checksum]: 2021-09-17T19:08:41Z Validating workflow
[shadow-disk-checksum]: 2021-09-17T19:08:41Z Validating step "create-disks"
[shadow-disk-checksum]: 2021-09-17T19:08:41Z Validating step "create-instance"
[disk-1-inflate]: 2021-09-17T19:08:41Z Step "import-virtual-disk" (CreateInstances) successfully finished.
[disk-1-inflate]: 2021-09-17T19:08:41Z Running step "wait-for-signal" (WaitForInstancesSignal)
[disk-1-inflate.wait-for-signal]: 2021-09-17T19:08:41Z WaitForInstancesSignal: Instance "inst-importer-disk-1-inflate-mtq9n": watching serial port 1, SuccessMatch: "ImportSuccess:", FailureMatch: ["ImportFailed:" "WARNING Failed to download metadata script" "Failed to download GCS path" "Worker instance terminated"] (this is not an error), StatusMatch: "Import:".
[disk-1-inflate.import-virtual-disk]: 2021-09-17T19:08:41Z CreateInstances: Streaming instance "inst-importer-disk-1-inflate-mtq9n" serial port 1 output to https://storage.cloud.google.com/GCP_PROJECT-ovf-import-bkt-us-central1/st3wt/ovf-st3wt-1/daisy-disk-1-inflate-20210917-19:08:20-mtq9n/logs/inst-importer-disk-1-inflate-mtq9n-serial-port1.log
[shadow-disk-checksum]: 2021-09-17T19:08:42Z Validating step "wait-for-checksum"
[shadow-disk-checksum]: 2021-09-17T19:08:42Z Validation Complete
[shadow-disk-checksum]: 2021-09-17T19:08:42Z Workflow Project: GCP_PROJECT
[shadow-disk-checksum]: 2021-09-17T19:08:42Z Workflow Zone: us-central1-f
[shadow-disk-checksum]: 2021-09-17T19:08:42Z Workflow GCSPath: gs://GCP_PROJECT-ovf-import-bkt-us-central1/st3wt/ovf-st3wt-1
[shadow-disk-checksum]: 2021-09-17T19:08:42Z Daisy scratch path: https://console.cloud.google.com/storage/browser/GCP_PROJECT-demo-ovf-import-bkt-us-central1/st3wt/ovf-st3wt-1/daisy-shadow-disk-checksum-20210917-19:08:41-j39zd
[shadow-disk-checksum]: 2021-09-17T19:08:42Z Uploading sources
[shadow-disk-checksum]: 2021-09-17T19:08:42Z Running workflow
[shadow-disk-checksum]: 2021-09-17T19:08:42Z Running step "create-disks" (CreateDisks)
[shadow-disk-checksum.create-disks]: 2021-09-17T19:08:42Z CreateDisks: Creating disk "disk-shadow-disk-checksum-shadow-disk-checksum-j39zd".
[shadow-disk-checksum]: 2021-09-17T19:08:43Z Step "create-disks" (CreateDisks) successfully finished.
```

And also see the new image created:

```bash
```