from setuptools import setup

setup(name="dodsbir",
	version='0.9.1',
	description='Scraping library for DODSBIR.net',
	url='http://github.com/jroo/dodsbir-scrape',
	author='18F.gsa.gov',
	zip_safe=False,
	install_requires = [
        'beautifulsoup4>=4.3.2',
		'requests==2.3.0'
	],
    packages=['dodsbir'],
    package_dir={'dodsbir': 'lib'},
    classifiers=['Development Status :: 2 - Pre-Alpha']
)
