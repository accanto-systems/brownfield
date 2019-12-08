# Brownfield Demo Setup

## Setup LM

Run the AIO_heat.yaml template to create a VM for the LM AIO. 

Clone [lm-allinone](https://github.com/accanto-systems/lm-allinone.git) project on the AIO VM and add your LM software source and helm charts to **lm-allnone/lm-artifacts** directory.

Update the following properties in **lm-allinone/ansible/ansible-variables.yml** file to point to LM software

```
lm_charts_package: ../lm-artifacts/lm-helm-charts-2.1.0-XXXX-dist.tgz
lm_docker_package: ../lm-artifacts/lm-docker-source-2.1.0-XXXX-dist.tgz
```

### Set the RM polling timer to 5 secs

Add the fillowing daytona block to the **lmConfigImport** section of the ansible/lm-helm-values.yml file

```
configurator:
  lmConfigImport:
    ...
    daytona:
      alm.daytona.resource-manager.polling-interval: 5000
```

### Theme LM if you need to

Add your theme tar file to **lm-allinone/ansible** directory and update the following properties in your **lm-allinone/ansible/ansible-variables.yml** file.

```
lm_theme: True
lm_theme_directory: .
lm_theme_name: bluerinse
```

### Run the AIO installation

### Dependencies

```
sudo apt-get install python3-pip
pip3 install ansible
```

To install AOI on your machine:

```
sudo apt-get install sshpass
sudo apt-get install python-apt
```

If you are installing on an existing Ubuntu box:

```
sudo service apparmor start
sudo apt-get purge apache2
```

Update the inventory as per instructions 

Create your AIO by running the following command:

```
ansible-galaxy install -r ansible/requirements.yml -p ansible/roles
ansible-playbook -i ansible/inventories/allinone/inventory ansible/start-aio.yml
```

## Setup LMCTL

Install lmctl on your host machine by running the folowing command:

```
python3 -m pip install lmctl
```

Create a file called **lmconfig.yaml** and add the following:

```
environments:
  dev:
    description: dev environment on BT
    alm:
      host: 192.168.10.5
      port: 8083
      protocol: https
      auth_host: 192.168.10.5
      auth_port: 8082
      username: jack
      password: jack
      secure: true
    arm:
      defaultrm:
        host: 192.168.10.5
        port: 31081
        protocol: https
```

In a command shell you need to set the following environment variable to point to this file. 
```
export LMCONFIG=~/lmconfig.yaml
```

## Install 2.1 Drivers

Log into the AIO box @ AIO_FLOATING_IP. Username/Password is ubuntu/ubuntu and run the following commands to attach required Resource Manager drivers. 

```
helm init
```

### Ansible lifecycle driver

Create an Ansible lifecycle driver by running the following commands in the AIO VM. 

Log into AIO_FLOATING_IP (ubuntu/ubuntu) and add Ansible driver micro service:

```
helm install --name ansible-lifecycle-driver https://github.com/accanto-systems/ansible-lifecycle-driver/releases/download/v0.4.0/ansiblelifecycledriver-0.4.0.tgz
```

On your host machine run the following lmctl command to add the ansible lifecycle driver micro service to the ALM resource manager. 

```
lmctl lifecycledriver add --type ansible --url http://ansible-lifecycle-driver:8293 dev
```

### Openstack HEAT driver

Create a VIM HEAT driver by running the following commands on the AIO virtual machine @ 192.168.10.5 (vagrant/vagrant).

```
helm install --name openstack-vim-driver https://github.com/accanto-systems/openstack-vim-driver/releases/download/0.3.0/os-vim-driver-0.3.0.tgz
```
On your host machine run the following lmctl command to attach the VIM driver to the resource manager.

```
lmctl vimdriver add --type Openstack --url http://os-vim-driver:8292 dev
```

## Add locations

### Openstack location

Once AIO is up and running, log onto LM at https://192.168.10.5:8082 and create the following locations. 

Add a location called "core" with resource manager "brent" and infrastructure type "Openstack" and provide the following properties

```
os_auth_project_name: admin
os_auth_project_domain_name: default
os_auth_password: password
os_auth_username: admin
os_auth_user_domain_name: default
os_auth_api: v3
os_api_url: http://192.168.10.10:5000
almip: AIO_FLOATING_IP
```


https://10.220.219.129/ui

## Add kafka viewer to AIO

https://github.com/lensesio/kafka-topics-ui

```
docker pull landoop/kafka-topics-ui
    docker run --rm -it -p 8000:8000 \
               -e "KAFKA_REST_PROXY_URL=http://kafka-rest-proxy-host:port" \
               -e "PROXY=true" \
               landoop/kafka-topics-ui
```

https://www.kafkamagic.com/