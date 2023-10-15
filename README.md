# hotrocks asphalt operations application

Version 1.0.0 is an asphalt daily job keeping system which sends order email to your operations coordinator

This has been written on python 3.11.

First clone the repository:
git clone https://github.com/agshadow/hotrocks

set up virtual environment:
python -m venv venv

install packages from requirements.
pip install -r requirement.txt

create .env file with the following:
emailUsername = "email@email.com"
emailPassword = "emailpassword"
adminPassword = "password hash" (werkzeug.security ->generate_password_hash)
PGUSER = "postgres username"
PGPWD = "postgres password"
PGPATH = "path to postgres server"

emailUsername is your gmail email address
emailPassword is the gmail app password -> google account -> security -> 2 step verification -> app passwords

use command line python to generate password_hash:
python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('Password'))"

note: any changes to the .env file, you will need to restart the server.

install dependencies from pyproject.toml:
pip install -e .

## How to run in development

run the app in debug mode:
flask --app hotrocks run --debug

## How to deploy to production

install dependencies from pyproject.toml:
note: you may need to delete instance directory for this to work.
pip install -e .

to build a wheel (not necessary for production at this stage)
pip install build
python -m build --wheel

run on a waitress server:
pip install waitress
waitress-serve --call 'hotrocks:create_app'

build docker container:
pip freeze > requirements.txt
remove redundant hotrocks from the requirements.txt

build docker container - if you have pip install -e . then remove it from the requirements.txt
Docker build -t hotrocks .

Then run the dockerfile on your local machine on 127.0.0.1:49160:
Docker run -it -p 49160:80 -d hotrocks

## set up Azure

create new container registry and copy the login server eg hotrocks.azurecr.io to paste below.

loginto Azure
docker login hotrocks.azurecr.io
username : host name of the registry ( from access keysin the azure cp)
password : the access key (may have to enable admin user)

build docker container and push it:
docker build -t hotrocks.azurecr.io/hotrocks:latest .
docker push hotrocks.azurecr.io/hotrocks:latest

now create a resource - webapp
select docker and other info
click next to docker
select azure container registry
and select free plan

once ths is created you should be able to view your web app.

now turn on the continous deployment:
Deployment -> deployment center contains the container settings
turn on continuous deployment and save

this continouous deployment creates a webhook resource which will fire which will fire each time we push a container.

now still in the webapp control panel go to settings->Configuration and add enviornment variables as [er the local .env file, dont forget to save it.

so once the webhook is runnings.

make whatever changes to the app code then build and push the repository.

docker build -t hotrocks.azurecr.io/hotrocks:latest .
docker push hotrocks.azurecr.io/hotrocks:latest

this should trigger the webhook.

## set up postgres database

i used elephant SQL. Create new database then set the user/pass and url in the .env file and in the azure container configuration (as per above)
