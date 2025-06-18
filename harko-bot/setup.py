from setuptools import setup, find_packages

setup(
    name="harko-bot",
    packages=find_packages(),
    version="1.0.0",
    license="LGPLv3",
    description="AI Powered Harkonnen Propaganda Discord Bot",
    author="eb3095",
    author_email="ebennerit@gmail.com",
    url="https://github.com/eb3095/harko-bot",
    requires=[
        "openai",
        "apscheduler",
        "requests"
    ],
    keywords=["dune", "harkonnen", "propaganda", "discord", "bot", "ai", "gpt-3.5-turbo", "gpt-4", "openai", "langchain", "llm", "harkonnen", "dune bot", "dune discord bot", "harkonnen discord bot", "harkonnen bot", "dune harkonnen bot", "dune harkonnen discord bot"],
)
