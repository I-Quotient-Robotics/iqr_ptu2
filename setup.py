from iqr_ptu2 import __version__

from setuptools import setup


setup(
    name='iqr_ptu2',
    description='IQR PTU2 SDK',
    url='https://github.com/I-Quotient-Robotics/iqr_ptu2',
    py_modules=['iqr_ptu2'],
    version=__version__,
    install_requires=[
        'pyserial',
        'pymodbus',
    ],
    license='MIT',
    author='haonan.yang',
    author_email='haonan.yang@iqr-robot.com'
)
