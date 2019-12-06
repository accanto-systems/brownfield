import sys
import logging
import yaml
import stacktransformer.transformer as transformer
import stacktransformer.openstack.environment as openstackenv

logger = logging.getLogger(__name__)

def main():
    logging.basicConfig()
    if len(sys.argv[1:]) != 3:
        raise ValueError('Need 3 args: STACK_ID TRANSFORM_FILE DEPLYOMENT_LOCATION_FILE')
    stack_id = sys.argv[1]
    transform_file = sys.argv[2]
    deployment_location_file = sys.argv[3]
    with open(transform_file, 'r') as stream:
        raw_transform_config = yaml.safe_load(stream)
    transform_jobs = []
    for entry in raw_transform_config:
        stack_name = entry.get('stack_name')
        heat_template_file = entry.get('heat_template')
        with open(heat_template_file, 'r') as stream:
            heat_template = stream.read()
        parameters = entry.get('parameters', {})
        transform_job = transformer.HeatTemplateTransformJob(stack_name, heat_template, parameters, [transformer.AutoResourceMatchTransformation()])
        transform_jobs.append(transform_job)
    with open(deployment_location_file, 'r') as stream:
        deployment_location = yaml.safe_load(stream)
    openstack_location = openstackenv.OpenstackDeploymentLocationTranslator().from_deployment_location(deployment_location)
    result = transformer.transform(openstack_location, stack_id, transform_jobs)
    for k,v in result.items():
        print('{0}: {1}'.format(k,v))

if __name__ == '__main__':
    main()
