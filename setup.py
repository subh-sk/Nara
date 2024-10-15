from setuptools import setup, find_packages
import os

version = "0.3.79"

# Read the long description from README.md
def get_long_description():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Parse requirements.txt for dependencies
def parse_requirements(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return file.read().splitlines()
    return ['rich',
    'mailtm',
    'pytz',
    'groq',
    'requests',
    'python-dotenv',
    'datetime',
    'aiohttp',
    'beautifulsoup4',
    'wheel',
    'setuptools',
    'Pillow',
    'telethon',
    'python-dotenv',
    'humanfriendly',
    'faker',]

# Fetch dependencies from requirements.txt
install_requires = parse_requirements('requirements.txt')

# Classifiers for PyPI
classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Intended Audience :: Developers',
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Software Development :: Testing",
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'Operating System :: Microsoft :: Windows :: Windows 11',
    'Operating System :: Unix',
    'Operating System :: MacOS :: MacOS X',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
    'Programming Language :: Python :: 3.12',
    'Programming Language :: Python :: 3.13',
    "Topic :: Scientific/Engineering :: Artificial Intelligence",
    "Topic :: Scientific/Engineering :: Image Processing",
    "Topic :: Scientific/Engineering :: Visualization",
    "Topic :: Software Development",
    "Topic :: Software Development :: Quality Assurance",
    "Topic :: Software Development :: Code Generators",
    "Topic :: Software Development :: Libraries",
    "Topic :: Software Development :: Libraries :: Application Frameworks",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Software Development :: Testing",
]

# Dynamic setup configuration
setup(
    name='nara',
    version=version,
    description="AI-driven real-time information retrieval, chatbot interactions, and more.",
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    url='https://github.com/subh-sk/Nara',
    author='Subhash Kumar, Divyansh Shukla, Yateesh Reddy',
    maintainer='Nara Developers',
    maintainer_email='naravirtualai@gmail.com',
    python_requires='>=3.10',
    license='MIT',
    classifiers=classifiers,
    install_requires=install_requires,
    
    # Automatically find packages inside the project
    packages=find_packages(include=['nara', 'nara.*']),
    
    include_package_data=True,  # Include additional files specified in MANIFEST.in

    keywords=[
        'nara',
        'ai',
        'template generator',
        'cloud storage',
        'temporary email',
        'SQL utilities',
        'datetime utilities',
        'fake data generation',
        'async tasks',
        'file management',
        'time utilities',
    ],

    project_urls={
        'Homepage': 'https://github.com/subh-sk/Nara',
        'Documentation': 'https://github.com/subh-sk/Nara/wiki',
        'Download': 'https://pypi.org/project/nara/#files',
        'Release notes': 'https://github.com/subh-sk/Nara/releases',
        'Source': 'https://github.com/subh-sk/Nara',
        'Tracker': 'https://github.com/subh-sk/Nara/issues',
    },
)
