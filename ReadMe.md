# Overview
This a replacement for [Django GraphQL Auth](https://github.com/PedroBern/django-graphql-auth) that works with latest Django and Graphene

## Quick Start

```bash
# clone the repo
git clone 
# install deps
pip install -r requirements.txt
# Build app
python setup.py sdist
# Install it
python -m pip install  dist/django-graph-auth-0.1.0.tar.gz
# Test app migrate
python testproject/manage.py migrate
# 
python testproject/manage.py runserver
# Install in a custom project
python -m pip install  path/to/dist/django-graph-auth-0.1.0.tar.gz

```


## TODO
- [ ] Update ReadMe
- [ ] Test the `Queries` i.e Me, UserStatus, User
- [ ] Test the `Mutations` i.e Register, Verify Account, Resend Activation, Send Password Reset, Verify Token, Password Reset, Login and Logout
- [ ] Add Documentation
- [ ] Test usage of `EMAIL_ASYNC_TASK` to send emails Asynchronously
- [ ] Add a Notify Admin Aysnc function that sends emails to admins when Exceptions occur
- [ ] Write Tests
- [ ] Package the app for Pypi


## Resources
- [Reusing Django Apps](https://docs.djangoproject.com/en/4.1/intro/reusable-apps/)
- [Installing Using Pip](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/)
