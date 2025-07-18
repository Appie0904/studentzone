"""
StudentZone - Nationwide Student Network for Dutch Higher Education

A Django-based platform designed to unite students in the Netherlands by field of study.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="studentzone",
    version="0.1.0",
    author="StudentZone Contributors",
    author_email="support@studentzone.nl",
    description="Nationwide Student Network for Dutch Higher Education",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Appie0904/studentzone",
    project_urls={
        "Bug Reports": "https://github.com/Appie0904/studentzone/issues",
        "Source": "https://github.com/Appie0904/studentzone",
        "Documentation": "https://github.com/Appie0904/studentzone#readme",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
        "Framework :: Django",
        "Framework :: Django :: 5.2",
        "Topic :: Education",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    python_requires=">=3.12",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.3",
            "pytest-django>=4.7.0",
            "coverage>=7.3.2",
            "django-debug-toolbar>=4.2.0",
            "django-extensions>=3.2.3",
        ],
        "production": [
            "gunicorn>=21.2.0",
            "whitenoise>=6.6.0",
            "psycopg2-binary>=2.9.9",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords="django, education, students, netherlands, collaboration, networking",
) 