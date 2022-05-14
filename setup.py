import os

import setuptools

requires = [
    "python-dotenv==0.20.0",
    "requests==2.27.1",
    "websockets==10.3",
]

with open("README.md", "r") as fh:
    long_description = fh.read()

about = {}
here = os.path.abspath(os.path.dirname(__file__))
with open(
    os.path.join(here, "pykorbit", "__metadata__.py"),
    mode="r",
    encoding="utf-8",
) as f:
    exec(f.read(), about)

setuptools.setup(
    name="pykorbit",
    version=about["__version__"],
    description="Python REST/WS API for Korbit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Bisonai",
    author_email="business@bisonai.com",
    url="https://github.com/bisonai/pykorbit",
    packages=["pykorbit"],
    package_dir={"pykorbit": "pykorbit"},
    python_requires=">=3.9, <4",
    install_requires=requires,
    zip_safe=False,
)
