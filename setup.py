import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bitbrowser_api",
    version="0.1",
    author="embzheng",
    author_email="embzheng@qq.com",
    description="This is a bitbrowser operation tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/embzheng/bitbrowser_api",
    packages=setuptools.find_packages(),
    install_requires=['playwright>=1.42.0','requests','wallet_tool'],    
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)