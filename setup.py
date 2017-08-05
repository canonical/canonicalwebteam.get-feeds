from setuptools import setup

setup(
    name='canonicalwebteam.get-feeds',
    version='0.1.6',
    author='Canonical Webteam',
    url='https://github.com/canonical-webteam/get-feeds',
    packages=[
        'canonicalwebteam',
        'canonicalwebteam.get_feeds'
    ],
    description=(
        'Functions and template tags for retrieving JSON '
        'or RSS feed content.'
    ),
    install_requires=[
        "Django >= 1.3",
        "requests-cache >= 0.4.0",
    ],
)

