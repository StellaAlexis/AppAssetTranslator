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
    url='https://github.com/StellaAlexis/AppAssetTranslator',
    install_requires=['pandas', 'PyYAML'],
    download_url='https://github.com/StellaAlexis/AppAssetTranslator',
    entry_points='''
        [console_scripts]
        app-asset-translator=app_asset_translator.translator_scripts:main
    '''
)
