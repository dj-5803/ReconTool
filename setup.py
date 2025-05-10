# setup.py
from setuptools import setup, find_packages

setup(
    name="recontool",
    version="1.0.1",
    python_requires='>=3.10, <3.13',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pyfiglet>=1.0,<2.0",
        "python-barcode>=0.15",
        "pyqrcode>=1.2,<2.0",
        "phonenumbers>=8.13,<9.0",
        "requests>=2.31,<3.0",
        "tabulate>=0.9,<1.0"
    ],
    entry_points={
        'console_scripts': [
            'recontool=app:main',
        ],
    },
)
