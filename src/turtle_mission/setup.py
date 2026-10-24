from setuptools import find_packages, setup

package_name = 'turtle_mission'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch',
    ['launch/mission.launch.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='yassin',
    maintainer_email='yassin@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'validate_server = turtle_mission.validate_server:main',
            'destination_client = turtle_mission.destination_client:main',
            'action_server = turtle_mission.action_server:main',
        ],
    },
)
