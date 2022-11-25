import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='backblazewrapper',
    version='0.0.1',
    author='Alex Q',
    author_email='alex.quan0807@gmail.com',
    description='Wrapper for Backblaze',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    packages=['backblazewrapper'],
    install_requires=[
        "b2sdk",
    ],
)