import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="telepost",
    version="0.0.11",
    author="Yunzhi Gao",
    author_email="gaoyunzhi@gmail.com",
    description="Get post from telegram and make ready to repost it to other places (twitter / douban / reddit).",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gaoyunzhi/telepost",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'telegram_util',
        'pyyaml',
        'webgram',
        'telethon',
    ],
    python_requires='>=3.0',
)