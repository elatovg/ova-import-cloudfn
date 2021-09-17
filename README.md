# ova-import-cloudfn

## Enable Prereqs
```
gcloud services enable cloudbuild.googleapis.com
```

Mirror Github repo to Cloud Source Repositories (All the instructions are laid out in [Mirroring a GitHub repository](https://cloud.google.com/source-repositories/docs/mirroring-a-github-repository))

## Create the function
The function will be triggered by an upload to a storage bucket:

```bash
export PROJECT_ID=$(gcloud config list --format 'value(core.project)')
export REGION="us-central1"
export GCS_BUCKET="elatov-demo-keys"
export CLOUD_SOURCE_REPO="github_elatovg_ova-import-cloudfn"
export SRC_PATH="https://source.developers.google.com/projects/${PROJECT_ID}/repos/${CLOUD_SOURCE_REPO}/moveable-aliases/main/paths/app"
export CLOUD_FN_NAME="build_ova"
gcloud functions deploy ${CLOUD_FN_NAME} --runtime python39 \
  --set-env-vars "PROJECT_ID=${PROJECT_ID}" \
  --trigger-bucket ${GCS_BUCKET} --entry-point main --region ${REGION} \
  --source ${SRC_PATH}
```