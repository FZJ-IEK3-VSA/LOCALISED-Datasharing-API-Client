"""Setup file for python packaging."""
import os
import setuptools

dir_path = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(dir_path, "README.md"), mode="r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="zoomin_client",
    version="0.1.0",
    author="Shruthi Patil",
    author_email="s.patil@fz-juelich.de",
    description="API client to access data from LOCALISED datasharing platform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.localised-project.eu/",
    include_package_data=True,
    packages=setuptools.find_packages(),
    setup_requires=["setuptools-git"],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.10",
        "Topic :: Database",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
    keywords=["localisation", "proxy metrics"],
)
