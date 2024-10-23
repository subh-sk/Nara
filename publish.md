# Upload Package

## Dependencies
`pip install setuptools wheel twine`

## Build Your Package
`python setup.py sdist bdist_wheel`


## Upload Your Package to Test PyPI (Optional)

1. Register on Test PyPI if you haven't already: [Test PyPI](https://test.pypi.org/account/register/)
2. `twine upload --repository-url https://test.pypi.org/legacy/ dist/*`
3. Install your package from Test PyPI to verify it works:
`pip install --index-url https://test.pypi.org/simple/ my_package
`

## Upload Your Package to PyPI
`python -m twine upload dist/*`

##
 