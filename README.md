# AI Assistant - Chatbot that can answer questions about you!

## 📚 Technical Description

This chatbot is built with Streamlit and Langchain as the chat engine in the backend. The current version uses the OpenAI chat model ("gpt-3.5-turbo") to generate responses, but it is very simple to change this option. Refer to the Langchain documentation for a full list of supported chat models.

## 🖥️ Configure Local Development Environment

### Prerequisites

- Python 3.11
- Poetry

### Install Local Python Environment

```bash
poetry install
```

### Run Unit Tests

```bash
poetry run pytest
```

## 🚀 Deployment

The chatbot is configured to be deployed to Cloud Run. Build steps are defined in `cloudbuild.yaml`.

Here are the steps to configure the CD pipeline to deploy the chatbot to your GCP project:

### Prerequisites:

- A GCP project with the following services activated: Cloud Run, Cloud Build, Secret Manager, Artifact Registry
- A bucket in this project to store Terraform states
- A secret to store your OpenAI API token
- A Docker repository for Docker images in Artifact Registry

### Configuration:

1. Fork this GitHub repository
2. Customize the chat prompt for your AI assistant: `src/prompt.txt`
3. Configure your bucket for Terraform states: `terraform/backend.tf`
4. Configure your project, region, and OpenAI key secret name in `terraform/locals.tf`
5. Configure your Docker repository (in Artifact Registry) in `cloudbuild.yaml`, section `substitutions`
6. In Cloud Build, create a trigger that listens to the `push to master` event of your GitHub repository. Detail instructions could be found here: https://cloud.google.com/build/docs/automating-builds/github/build-repos-from-github?generation=2nd-gen
