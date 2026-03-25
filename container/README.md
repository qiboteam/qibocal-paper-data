# Qibocal reproduction container

In the accompanying folder, two files are provided: an Apptainer container definition
and a Jupyter notebook. The container definition ensures the installation of a specific,
verified version of Qibocal, while the notebook demonstrates the functionality of the
environment using the built-in simulator integration.

While Qibocal is designed for installation via pip and is intended to function
seamlessly with this method, the provided container serves as a reference implementation
to confirm the feasibility of a fully operational environment. Additionally, it
facilitates experimentation by mitigating potential incompatibilities among
dependencies, which, although not expected, may occasionally arise.

## Pre-built image

The built image has been deployed in GitHub Packages registry. To use it, just pull with
`apptainer`, setting your GitHub credentials with suitable environment variables.

```sh
export APPTAINER_DOCKER_USERNAME="<username>"
export APPTAINER_DOCKER_PASSWORD="<token>"
apptainer pull oras://ghcr.io/qiboteam/qibocal-paper:latest
```

- `<username>` is the name of the GitHub account, as found in your profile page URL,
  after `github.com/` (e.g. `qiboteam` in `https://github.com/qiboteam/`)
- `<token>` is a personal access token (PAT, classic), with the `read:packages`
  permission
  - https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-personal-access-token-classic
  - https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/scopes-for-oauth-apps#available-scopes
