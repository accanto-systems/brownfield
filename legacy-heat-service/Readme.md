# Legacy VoIP Service

Either through horizon or CLI create the legacy heat template

e.g. openstack heat create heat-template.yaml??

Update the inventory.yaml file with the required ip addresses created by the heat template

run the ansible playbooks to configure the vms and start the service with the following command

ansible-playbook -i inventory.yaml start.yaml