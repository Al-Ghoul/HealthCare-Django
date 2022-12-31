# HealthCare
## A Disease Symptoms analyzer writter purely in python.

## All Data were imported from the health-care chatbot, credit go to the rightful owner.
### Repo link --> https://github.com/itachi9604/healthcare-chatbot
## Tech

HealthCare uses a number of open source projects to work properly:

- [Django] - The web framework for perfectionists with deadlines.
- [Python] - Python is a programming language that lets you work quickly
and integrate systems more effectively.

## Installation

HealthCare requires [Python](https://www.python.org/) v3.10.8+ to run.

Clone this repo on ur local machine...

```sh
git clone https://github.com/Al-Ghoul/HealthCare-Django.git
```

Change your directory to the repo, create the virtual env and activate your venv...
```sh
cd HealthCare-Django
py -m venv YOUR_VENV_NAME
venv\Srcripts\activate
```

Install the dependencies and start the server.

```sh
pip install -r .\requirements.txt
cd HealthCare
py manage.py runserver PORT
```
# NOTE if you are not on windows OS, replace 'py' with 'python', and finally either way replace 'PORT' with the port you'd like, normally I'd go with 80.