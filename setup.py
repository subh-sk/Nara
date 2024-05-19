from setuptools import setup, find_packages

VERSION = '0.1'

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
    name='Nara',
    version=VERSION,
    description="A versatile package for AI-based real-time information and chatbot interactions, creating temporary emails, generating random data, caching, and JSON manipulation.",
    long_description=open('README.md').read(),  # Assuming the README file is in Markdown format
    long_description_content_type='text/markdown',
    url='https://github.com/subh-sk/Nara',
    author='Subhash Kumar, Divyansh Shukla, Yateesh Reddy',
    maintainer='Nara Developers',
    maintainer_email='naravirtualai@gmail.com',
    python_requires='>=3.10',
    license='MIT',
    classifiers=classifiers,
    install_requires=[
        'mailtm',
        'rich',
        'requests',
        'mimesis',
        'faker',
        'groq'
        # 'numpy',
        # 'pandas',
        # 'scipy',
        # 'scikit-learn',
        # 'tensorflow',
        # 'torch',
        # 'transformers',
    ],
    # packages=find_packages(),
    packages=[
        'Nara',
        'Nara.nara',
        'Nara.Extra',
        'Nara.Extra.TempMail',
        'Nara.Extra.Json',
    ],
    keywords=['ai','templategenerator','template generator','code generation', 'temp mail', 'ai chat', 'nara', 'nara ai', 'json','fakename','fakeid'],
    project_urls={
        'Homepage': 'https://github.com/subh-sk/Nara',
        'Documentation': 'https://github.com/subh-sk/Nara/wiki',
        'Download': 'https://pypi.org/project/nara/#files',
        'Release notes': 'https://github.com/subh-sk/Nara/releases',
        'Source': 'https://github.com/subh-sk/Nara',
        'Tracker': 'https://github.com/subh-sk/Nara/issues',
    }
)
