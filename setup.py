"""setup.py""" 

from setuptools import setup, find_packages

setup(
    name="dbfunk",  # Paket nomi
    version="0.1.0",  # Paket versiyasi
    description="A library for managing SQLite database tables and data",  # Paketning qisqacha tavsifi
    author="nxscoder",  # Muallif ismi
    author_email="dasturchixurshid@gmail.com",  # Muallifning elektron pochta manzili
    license="MIT",  # Litsenziya
    packages=find_packages(where="src"),  # src papkasida joylashgan paketlarni topish
    package_dir={"": "src"},  # Paketlar src papkasidan izlanadi
    classifiers=[  # PyPI uchun tasniflar
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[  # Agar kutubxona boshqa kutubxonalarga bog'liq bo'lsa, ular shu yerga yoziladi
        # Masalan, sqlite3 odatda Python bilan keladi, shuning uchun qo'shish shart emas.
    ],
    python_requires='>=3.6',  # Python versiyasi
)

