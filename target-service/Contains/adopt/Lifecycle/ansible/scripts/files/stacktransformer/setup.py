from setuptools import setup, find_namespace_packages

setup(
    name='stack-transformer',
    version='0.0.1',
    author='Accanto Systems',
    description='Transform large stacks into smaller stacks',
    packages=find_namespace_packages(include=['stacktransformer*']),
    include_package_data=True,
    install_requires=[
        'python-heatclient>=1.17.0,<2.0',
        'python-keystoneclient>=3.19.0,<4.0'
    ],
    entry_points='''
        [console_scripts]
        lmctl=lmctl.cli.entry:init_cli
    '''
)
