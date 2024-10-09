from setuptools import setup, find_packages

setup(
    name="my_elastic_package",  # Название пакета
    version="0.1",
    packages=find_packages(),  # Автоматический поиск всех пакетов
    install_requires=[
        'elastic-transport==8.15.0', 
        'elasticsearch==8.15.1'
    ],
    description="Модуль взаимодействия с ElasticSearch",
    author="Дмитрий Прокофьев",
    author_email="",
    url="https://github.com/DmitryProkofev/elastic_package.git",  # Ссылка на репозиторий (если есть)
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9.7',
)