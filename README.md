# sf_integration

The project includes integration with salesforce, and for now we can fetch account, user, and contacts
information using API's.


# Find URl's for fetch Account, User and contact list.

* For fetch accounts - http://localhost/accounts/
* For fetch users - http://localhost/users/
* For fetch contacts - http://localhost/contacts/


# Steps to install and run sf_integration on your local machine
* Run `$ pip install virtualenv` command to install virtual environment
* Run `$ virtualenv env -p python3.9` command to Create Virtual environment
* Run `$ source env/bin/activate` command to activate virtual environment
* Run `$ cd sf_integration` command for jump into the project directory
* Run `$ pip install -r requirements.txt` command to Install project requirement file


# Update setting variable with salesforce credential.

* `SF_CLIENT_ID = "Add Your Consumer Key here"`,
* `SF_CLIENT_SECRET = "Add Your Consumer Secret Key here"`,
* `SF_USERNAME = "Add Your salesforce username here"`,
* `SF_PASSWORD = "Add Your salesforce password her"`,
* `SF_BASE_URL = "Add your salesforce base url"`,