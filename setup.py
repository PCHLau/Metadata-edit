from setuptools import setup
setup(
    name='music',
    version='0.0.1',
    entry_points={
        'console_scripts': [
            'music=package:test.downloader'
        ]
    }
)