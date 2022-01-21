import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
  long_description = fh.read()

setuptools.setup(
  name="twitchbot",
  version="0.0.2",
  author="mrquokka",
  author_email="mrquokka@yandex.ru",
  description="Twitch API bot",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/mrquokka/twitchbot",
  project_urls={
    "Bug Tracker": "https://github.com/mrquokka/twitchbot/issues",
  },
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
  package_dir={"": "src"},
  packages=setuptools.find_packages(where="src"),
  install_requires=['twitchio'],
  python_requires=">=3.6",
)
