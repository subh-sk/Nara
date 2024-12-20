from setuptools import setup, find_packages

VERSION = '0.5'


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    
get_requirements = lambda: open('requirements.txt').read().splitlines()

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

setup(
    name='nara',
    version=VERSION,
    description="nara provides AI-driven real-time information retrieval,all in one sytanx of diffrent models, chatbot interactions, temporary email creation, random data generation, caching, JSON manipulation, async task handling, and structured threading.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/subh-sk/Nara',
    author='Subhash Kumar, Divyansh Shukla, Yateesh Reddy',
    maintainer='Nara Developers',
    maintainer_email='naravirtualai@gmail.com',
    python_requires='>=3.10',
    license='MIT',
    classifiers=classifiers,
    install_requires=get_requirements(),
    packages=[
    'nara',
    'nara.nara',
    'nara.llm',
    'nara.nara.classification',
    'nara.nara.genration',
    'nara.nara.tele_cloude_storage',
    'nara.extra',
    'nara.extra.async_task',
    'nara.extra.date_time',
    'nara.extra.extended_json',     
    'nara.extra.extended_sql',      
    'nara.extra.extended_sql.queue',
    'nara.extra.fake',
    'nara.extra.file_manager',      
    'nara.extra.prompt',
    'nara.extra.temp_mail',
    'nara.extra.tools',
],

    keywords = [
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
    }
)
