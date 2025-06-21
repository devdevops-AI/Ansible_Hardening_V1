FROM registry.access.redhat.com/ubi8/ubi

RUN dnf install -y python3 python3-pip \
    && pip3 install --no-cache-dir ansible-core==2.17 \
    && dnf clean all

WORKDIR /runner
COPY . /runner
CMD ["ansible-playbook", "-i", "inventory/hosts.yml", "rhel8_hardening.yml"]
