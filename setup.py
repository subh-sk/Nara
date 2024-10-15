from setuptools import setup, find_packages
import os

# Get the version dynamically (from environment variable or file)
def get_version():
    version = os.getenv("NARA_VERSION", "0.3.2")
    return version

# Read the long description from README.md
def get_long_description():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Package requirements
install_requires = [
    'rich',
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
    'faker',
]

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
    version=get_version(),
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
