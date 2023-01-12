from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Prometheus FastApi Pusher'
LONG_DESCRIPTION = 'Prometheus FastApi Pusher'

setup(
    name="fastapi_prometheus_pusher",
    version=VERSION,
    author="dreamhunter2333",
    author_email="<dreamhunter2333@gmail.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "prometheus-client"
    ],
    keywords=['python'],
    classifiers=[
        "Programming Language :: Python :: 3"
    ]
)
