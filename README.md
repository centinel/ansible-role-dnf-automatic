# Ansible Role: dnf-automatic

![License](https://img.shields.io/github/license/centinel/ansible-role-dnf-automatic) ![Build Status](https://img.shields.io/gitlab/pipeline/centinel-foss/ansible-role-dnf-automatic/master)

This [Ansible](https://www.ansible.com) project is a [role](https://docs.ansible.com/ansible/latest/user_guide/playbooks_reuse_roles.html) that can manage [dnf-automatic](https://dnf.readthedocs.io/en/latest/automatic.html), an automatic update management tool for Red Hat-based Linux distributions.

## Requirements

This role can manage remote hosts that use the operating systems listed below.

| **Operating System** | **Supported Versions** |
| ------ | ------ |
| CentOS | 8 or later|
| Fedora | 30 or later| 

The role has been tested on the Ansible versions listed below.

* 2.8
* 2.9
* devel (the upcoming version of Ansible)

## Installation

Assuming that you have Ansible [installed](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html), you can install this role to your workstation with the `ansible-galaxy` command as shown below.

    ansible-galaxy install centinel.dnf-automatic
    
If you're using [Ansible Tower](https://www.ansible.com/products/tower) or [AWX](https://github.com/ansible/awx), you can add this to your [project](https://docs.ansible.com/ansible-tower/latest/html/userguide/projects.html) by including the line below in your `requirements.yml` file.

    - src: centinel.dnf-automatic
      version: 1.0.0
      
Be sure to specify a version. If you don't, a future update may break things before you've had a chance to test the changes.
    
## Role Variables

The available variables are listed below along with the default values, which are defined in `defaults/main.yml` unless indicated otherwise.

**Install Settings**

| Name           | Default Value | Variable Type | Description                        |
| -------------- | ------------- | ------------- | -----------------------------------|
| `dnf_automatic_manage` | false | Boolean | Whether to manage dnf-automatic with this role.|

**Config Settings**

 Name           | Default Value | Variable Type | Description                        |
| -------------- | ------------- | ------------- | -----------------------------------|
| `dnf_automatic_template` | automatic.conf.j2 | String | Name of the template file to be used for creating `automatic.conf`, the dnf-automatic config file. Defaults to the template included with this role.|  
| `dnf_automatic_config_settings` | (See below.) | Dictionary | The configuration settings to be used in `dnf-automatic.conf`. Defaults to checking for available updates and emailing the `root` user.|

```
dnf_automatic_config_settings:
  commands:
    apply_updates: false
    download_updates: false
    upgrade_type: "default"
    random_sleep: "0"
  emitters:
    emit_via: "stdio"
    system_name: "{{ ansible_fqdn }}"
  command:
    command_format: "cat"
    stdin_format: "{body}"
  command_email:
    command_format: "mail -s {subject} -r {email_from} {email_to}"
    stdin_format: "{body}"
    email_from: "root"
    email_to: "root"
  email:
    email_from: "root"
    email_to: "root"
    email_host: "localhost"
  base:
    plugins: false
```

**Service Settings**

| Name           | Default Value | Variable Type | Description                        |
| -------------- | ------------- | ------------- | -----------------------------------|
| `dnf_automatic_timer` | dnf-automatic.timer | String | The [systemd timer](https://wiki.archlinux.org/index.php/Systemd/Timers) to run dnf-automatic. Defaults to behaving as `dnf_automatic_config_settings` indicates. Dnf-automatic comes with a few pre-configured [alternatives](https://dnf.readthedocs.io/en/latest/automatic.html#synopsis).|
| `dnf_automatic_timer_state` | started | String | The desired systemd state for `dnf_automatic_timer`.|
| `dnf_automatic_timer_enabled` | true | Boolean | Whether `dnf_automatic_timer` should auto-start on boot.|

# Dependencies

None.

# Example Playbook

Installs dnf-automatic with the default settings.

```
- hosts: centos-servers
  vars:
    dnf_automatic_manage: true
  roles:
    - centinel.dnf-automatic
```

Installs dnf-automatic and configures it to automatically download and install security updates.

```
- hosts: centos-servers
  vars:
  dnf_automatic_config_settings:
    commands:
      apply_updates: true
      download_updates: true
      upgrade_type: "security"
      random_sleep: "0"
    emitters:
      emit_via: "stdio"
      system_name: "{{ ansible_fqdn }}"
    command:
      command_format: "cat"
      stdin_format: "{body}"
    command_email:
      command_format: "mail -s {subject} -r {email_from} {email_to}"
      stdin_format: "{body}"
      email_from: "root"
      email_to: "root"
    email:
      email_from: "root"
      email_to: "root"
      email_host: "localhost"
    base:
      plugins: false
```

## Testing

[Molecule](https://molecule.readthedocs.io/en/stable/) and [Tox](https://tox.readthedocs.io/en/latest/) are used to run tests on this repository. Molecule tests running the role on different operating systems, and Tox tests running the role using different versions of Ansible.

[GitLab CI](https://docs.gitlab.com/ee/ci/) runs these tests on every commit. Tests are run periodically to ensure that the role still works as its supported components are updated.

You can also run these tests on your local workstation as necessary for development. Three arguments are supported, which you can change by prefixing your test command with `argument=value`.

* **namespace**: The Docker namespace to use. Defaults to `geerlingguy`, the Docker Hub account for Jeff Geerling, author of [Ansible for DevOps](https://www.ansiblefordevops.com/). (I'm not paid to say that, I swear!)
* **image**: The Docker image to use. Defaults to `centos8`.
* **tag**: The Docker registry tag to use. Defaults to `latest`.

```
# Tests via Molecule using the default settings - a CentOS 8 image.
molecule test

# Tests via Molecule on all supported operating systems at once
molecule test -s all

# Tests via Molecule using a custom container
namespace="someguy" image="centostesting" molecule test

# Tests via Tox using the default settings - a CentOS 8 image. Tests each supported version of Ansible sequentially.
tox

# Runs Tox tests on CentOS 8. Tests all supported versions of Ansible simultaneously.
image=centos8 tox --parallel all

```

## See Also

* **[Configuration File Format](https://dnf.readthedocs.io/en/latest/automatic.html#configuration-file-format)**: A complete listing of the available configuration settings for `automatic.conf`.

## License

Apache License, 2.0.

# Author Information

This role was created in 2019 by [Justin Smith](mailto:justin@adminix.net).
