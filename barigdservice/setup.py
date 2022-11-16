from setuptools import setup, find_packages

VERSION = '1.0' 
DESCRIPTION = 'A simple tool to manage Google Drive files'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="barigdservice", 
        version=VERSION,
        author="Bari BGF",
        author_email="bougafa.005@gmail.com",
        description=DESCRIPTION,
        packages=find_packages(),
        install_requires=["google-api-python-client", "google-auth-httplib2", "google-auth-oauthlib"],
        
        keywords=['python', 'googledrive', 'api'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
            "Operating System :: LinuxOS :: Linux",
        ]
)