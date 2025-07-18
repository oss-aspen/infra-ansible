# OSPO Infrastructure Management

This repository contains Ansible playbooks and roles for deploying and managing infrastructure for [Augur](https://github.com/chaoss/augur) and [8Knot](https://github.com/oss-aspen/8Knot) services in production (EC2 instances).


## Overview
Ansible is a powerful automation tool for managing and configuring server infrastructure, eliminating the need for manual setup and configuration of potentially many servers. In Ansible you define changes to the system by asserting what you want the result to be. This allows ansible to only make changes if they are needed. These assertions are stored in simple YAML files and can be organized into "playbooks", "roles", and "tasks" to help automate anything from large processes, small categories and individual services, or specific actions.


## Configuration Structure

**Playbooks**

This repository is organized with all the high-level processes defined in playbooks within the `playbooks` folder. This includes things like installing 8Knot, installing augur, upgrading a system's apt packages, performing backups, etc.

See each individual .yml file in this folder to read more about what it is for.

**Roles and Tasks**
In order to improve maintainability and reuse of common processes, these playbooks refer to "roles", which are a slightly more granular way to group things in ansible. These are located in the `roles` folder and contain various configuration items for the different services (augur, 8knot, etc).

Within these roles there are files that define specific `tasks`. These files are where the actual definitions for the actions being performed usually live, broken up granularly enough to allow them to be reused by multiple playbooks or even other tasks as needed.

**Inventory**
The `inventory/inventory.ini` file defines which machines are available to run ansible playbooks against. These can be grouped for more easily identifying multiple machines to apply these same processes to (if we wanted to host more than one of each service).

**Configuration**
the `ansible.cfg` file defines configuration items that help ansible know where to find things, such as the roles and inventory files, so that using ansible can be easier and more automatic. While you *can* put configuration specific to your machine in there, it would be preferred to put these items in `~/.ansible.cfg` or some [other config location](https://docs.ansible.com/ansible/latest/reference_appendices/general_precedence.html#configuration-settings) since this config file is shared by everyone who uses these ansible scripts.

## Quick Start

### Prerequisites

1. **Ansible** installed on your control machine (i.e. the one you are probably reading this from)
2. **AWS credentials** configured (for EBS operations)
3. **Vault password** for encrypted secrets
4. **SSH access** to target servers

### Setup

Many parts of this script require access to secrets. Some of these (like your SSH key) may already be set up for allowing you to access the services, others, like AWS access and the ansible vault password, are things you may need additional approval to access.

The main way secrets are stored in this repository is using ansible vault - this encrypts any secret values such that they can only be read (and thus used in playbooks) when you have the password. To learn more about using ansible vault, check out [this digitalocean primer](https://www.digitalocean.com/community/tutorials/how-to-use-vault-to-protect-sensitive-ansible-data).
