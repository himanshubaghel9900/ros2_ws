from setuptools import find_packages, setup

package_name = 'ugv_description'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        (
            'share/ament_index/resource_index/packages',
            ['resource/ugv_description']
        ),
        (
            'share/ugv_description',
            ['package.xml']
        ),
        (
            'share/ugv_description/launch',
            ['launch/ugv_sim.launch.py']
        ),
        (
            'share/ugv_description/urdf',
            ['urdf/ugv.urdf.xacro']
        ),
        (
            'share/ugv_description/rviz',
            ['rviz/ugv.rviz']
        ),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='himanshu',
    maintainer_email='himanshu@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'ugv_simulator = ugv_description.ugv_simulator:main',
        ],
    },
)
