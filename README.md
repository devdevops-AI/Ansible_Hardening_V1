# Ansible Hardening Example

This repository contains a basic example for hardening a RHEL 8 system using Ansible.
It includes a container image that installs `ansible-core==2.17`, a sample playbook, a
custom callback plugin that renders results to HTML, and an inventory with host
location metadata.

## Build the Docker image

```bash
podman build -t rhel8-ansible .
```

## Run the playbook inside the container

```bash
podman run --rm -v $(pwd):/runner rhel8-ansible
```

After execution an `hardening_report.html` file will be generated summarizing the
results by host location.
