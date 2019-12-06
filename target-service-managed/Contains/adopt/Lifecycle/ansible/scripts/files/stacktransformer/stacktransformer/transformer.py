import yaml
import json
import logging

def transform(openstack_location, stack_id, transform_jobs):
    heat_driver = openstack_location.heat_driver
    abandon_result = heat_driver.abandon_stack(stack_id)
    abandon_file = 'abandon_{0}.json'.format(stack_id)
    with open(abandon_file, 'w') as f:
        json.dump(abandon_result, f)
    logging.info('Abandon result written to {0}'.format(abandon_file))
    new_stacks = {}
    for job in transform_jobs:
        adoption = {
            'stack_user_project_id': abandon_result.get('stack_user_project_id', None),
            'environment': {},
            'project_id': abandon_result.get('project_id', None),
            'resources': {},
            'template': {}
        }
        new_stack_id = job.run(heat_driver, abandon_result, adoption)
        new_stacks[job.stack_name] = new_stack_id 
    return new_stacks
           


class HeatTemplateTransformJob:
    """
    Sets a new Heat template on the adoption, transforms elements of the original stack to fit into the new stack
    """
    
    def __init__(self, stack_name, heat_template, parameters, transformations):
        self.stack_name = stack_name
        self.heat_template = heat_template
        self.parameters = parameters
        self.transformations = transformations

    def run(self, heat_driver, abandon_result, adoption):
        parsed_template = yaml.safe_load(self.heat_template)
        if type(parsed_template['heat_template_version']) is not str:
            parsed_template['heat_template_version'] = parsed_template['heat_template_version'].strftime("%Y-%m-%d")
        adoption['template'] = parsed_template
        for transformation in self.transformations:
            transformation.run(abandon_result, adoption)
        adoption_file = 'adopt_{0}.json'.format(self.stack_name)
        with open(adoption_file, 'w') as f:
            json.dump(adoption, f, default=str)
        logging.info('Adoption file written to {0}'.format(adoption_file))
        stack_id = heat_driver.adopt_stack(self.stack_name, json.dumps(adoption), input_properties=self.parameters)
        return stack_id

class AutoResourceMatchTransformation:
    """
    Adopt any Resource which matches, by name, a Resource needed in the Heat template
    """

    def __init__(self):
        pass

    def run(self, abandon_result, adoption):
        resources_potentially_needing_adoption = self.__get_resources_potentially_needing_adoption(adoption)
        self.__adopt_abandoned_resources(resources_potentially_needing_adoption, abandon_result, adoption)

    def __get_resources_potentially_needing_adoption(self, adoption):
        adoption_template = adoption.get('template', None)
        if adoption_template is not None:
            template_resources = adoption_template.get('resources', None)
            if template_resources is not None:
                return list(template_resources.keys())
        return None

    def __adopt_abandoned_resources(self, resources_potentially_needing_adoption, abandon_result, adoption):
        if len(resources_potentially_needing_adoption) == 0:
            return None
        abandoned_resources = abandon_result.get('resources', {})
        for abandoned_resource_name, detail in abandoned_resources.items():
            if abandoned_resource_name in resources_potentially_needing_adoption:
                adoption['resources'][abandoned_resource_name] = detail

    
