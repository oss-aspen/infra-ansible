# OSPO Infrastructure Management

This repository contains Ansible playbooks and roles for deploying and managing infrastructure for [Augur](https://github.com/chaoss/augur) and [8Knot](https://github.com/oss-aspen/8Knot) services in production (EC2 instances).


## Overview
Ansible is a powerful automation tool for managing and configuring server infrastructure, eliminating the need for manual setup and configuration of potentially many servers. In Ansible you define changes to the system by asserting what you want the result to be. This allows ansible to only make changes if they are needed. These assertions are stored in simple YAML files and can be organized into "playbooks", "roles", and "tasks" to help automate anything from large processes, small categories and individual services, or specific actions.
