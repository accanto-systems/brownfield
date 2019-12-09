# Legacy VoIP Service

Either through horizon or CLI create the legacy heat stack with **heat-template.yaml**

Update the inventory.yaml file with the required ip addresses created by the heat template

run the ansible playbooks to configure the vms and start the service with the following command

```
ansible-playbook -i inventory.yaml start.yaml
```

Check that everything is working by logging onto the sipp VM and checking metrics are being captured