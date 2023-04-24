import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='app_asset_translator',
    packages=['app_asset_translator'],
    version='0.0.1',
    license='GNU GPLv3',
    description='Filler description',
    long_description=long_description,
    author='Myler Media',
    author_email='developers@mylermedia.nl',
    # TODO: Change to new public url
    url='https://gitlab.com/mylermediadevelopers/internal/translation-manager-python',
    install_requires=['pandas', 'PyYAML'],
    # TODO: Update to source code link
    download_url='url/to/source/code',
    entry_points='''
        [console_scripts]
        app-asset-translator=app_asset_translator.scripts.translator_scripts:main
    '''
)
