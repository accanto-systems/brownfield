# Running the demo


## Install VoIP manually

In visual studio
* Show HEAT template
* Show playbooks that configure the applications and start the service running

Instantiate HEAT template
* In Horizon UI, upload template and show it being created
* Show resources created in network topology

Activate Network Service
* run ansible-playbook -i inventory.yaml start.yaml
* log into SIPP and Asterisk consoles in Horizon and show processes runing and traffic flowing
* In asterisk show connections
* In sipp show metrics returned
* In kafka show metrics/traffic flowing

## Create ALM model to take over the network service

* lmctl creates a project with 4 resources, two versions of a Network service assembly
* Add target HEAT templates to each resource
* Add ansible scripts to each resource lifecycle
* Add the HEAT templates to adopt in the Adoption Job Resource
* In designer model the target network service
* In designer model the adoption version of the network service

## Takeover the network service

* Run the takeover behaviour scenario with the stack id to take over
* Show traffic running in DOKI
* Show execution plan
* Show the new stacks being created in horizon UI, showing the HEAT templates and that the resources are unaffected and traffic is still flowing
* Show the execution plan that upgrades the network service to remove the adoption job
* Asterisk health is now also monitored in DOKI which drives astersk resource healing policies

## Heal component of the network service

* Log onto asterisk, run pgrep and kill its process
* Show dropped calls in DOKI and failing health
* Show Healing policy automatically triggered in ALM UI
* run pgrep again on asterisk console and show its a different PID
* Show all call metrics now being successful in DOKI 