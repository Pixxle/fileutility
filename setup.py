import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
     name='fileutility',  
     version='0.6',
     author="Dennis Hedlund",
     author_email="dennishedlund@gmail.com",
     description="Helper module for locating and deleting files and folders.",
     long_description=long_description,
   long_description_content_type="text/markdown",
     url="https://github.com/Pixxle/fileutility",
     packages=['fileutility'],
     zip_safe=False,
     classifiers=[
         "Programming Language :: Python :: 2",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )
