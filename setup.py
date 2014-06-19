from setuptools import setup

setup(name="dodsbirscrape",
	version='0.8',
	description='Scraping library for DODSBIR.net',
	url='http://github.com/jroo/dodsbir-scrape',
	author='18F.gsa.gov',
	zip_safe=False,
	install_requires = ['beautifulsoup4>=4.3.2',
		'requests==2.3.0'
	]
)
