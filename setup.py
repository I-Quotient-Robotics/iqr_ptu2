from setuptools import setup

setup(
    name='iqr_ptu2',
    description='IQR PTU2 SDK',
    py_modules=['iqr_ptu2'],
    version='0.1',
    install_requires=[
        'pyserial',
        'pymodbus',
    ],
    license='MIT',
    author='haonan.yang',
    author_email='haonan.yang@iqr-robot.com'
)
