# setup.py en la raíz
from setuptools import setup, find_packages

setup(
    # ...
    install_requires=[
        'flask',
        'python-dotenv',
        'supabase',
        'openai',
        'twilio'
    ]
) 

setup(
    name="nexiapp",
    version="0.1",
    packages=find_packages(),
    package_dir={'': '.'},  # Buscar paquetes en el directorio actual
    include_package_data=True,
)