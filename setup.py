import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
project_urls = {
  'Source': 'https://github.com/embzheng/bitbrowser_api'
}
setuptools.setup(
    name="bitbrowser_api",
    version="0.4",
    author="blue",
    author_email="embzhengblue@gmail.com",
    description="This is a bitbrowser operation tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ox-blueblue/bitbrowser_api",
    packages=setuptools.find_packages(),
    install_requires=['playwright>=1.42.0','requests','wallet_tool','my_logtool'],    
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    project_urls = project_urls
)