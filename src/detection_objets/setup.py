from glob import glob
import os

from setuptools import find_packages, setup

package_name = 'detection_objets'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='assia',
    maintainer_email='assia@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
           # NODE_NAME = PACKAGE.FILE:main
           'camera_node = detection_objets.node_camera:main', 
           'detector=detection_objets.detection:main',
           'clusterer=detection_objets.clusterer:main',
           'intensity_filter=detection_objets.node_lidar:main',
           'transformer=detection_objets.transformer:main',
           'clusterer1=detection_objets.clusterer1:main',

        ],
    },
)
