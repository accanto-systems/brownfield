# Building a SIPP OpenStack image

## Pre-requisites

* A running OpenStack environment
* [Ubuntu Xenial image](http://cloud-images.ubuntu.com/xenial/current/xenial-server-cloudimg-amd64-disk1.img) pre-loaded to your OpenStack.
* Ensure you have a private neutron network connected to a router which is bound to a public network. Packer will deploy a build VM to this private network.
* The security group specified must have the ssh port open for packer to communicate with the VM it creates. 
* Create a new keypair and store the private key file on your local machine. 

## Configure your packer script

In the **sipp.json** and **asterisk.json** packer scripts, set the following ids from your openstack deployment.

```
  "identity_endpoint": "http://<YOUR OPENSTACK>/identity/v3",
  "tenant_name": "<YOUR OPENSTACK TENANT NAME>",
  "username": "<YOUR OPENSTACK USERNAME>",
  "password": "<YOUR OPENSTACK PASSWORD>",
  "networks": ["<PRIVATE NETWORK>"],
  "floating_ip_network":"<PUBLIC NETWORK>",
  "ssh_keypair_name": "<KEYPAIR NAME>",
  "ssh_private_key_file":"<KEYPAIR PEM>", 
  "source_image": "<XENIAL IMAGE ID>",
  "security_groups":["<YOUR SECURITY GROUP>"],
```

## Create the Asterisk Image

Download [Asterisk](https://downloads.asterisk.org/pub/telephony/asterisk/old-releases/asterisk-14.7.8.tar.gz) to software/ directory.

Run the following command to build the pbx image.

```
packer build asterisk.json
```

## Create the SIPP Image

Download [SIPP](https://github.com/SIPp/sipp/releases/download/v3.5.2/sipp-3.5.2.tar.gz) to software/ directory.

Run the following command to build the pbx image.

```
packer build sipp.json
```

## Retrieve the image to your local machine

Once the packer process is finished you can retrieve the image from you openstack environment by running the following command. 

```
glance image-download sipp
glance image-download ip-pbx
```

You can push this to your CICD Hub image repository to be used in other OpenStack instances.
