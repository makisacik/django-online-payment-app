# About

This Online Payment Service project is developed using Django, SQLite, and various Django built-in features for security and data handling. It enables users to view transactions, make payments,
request payments, and provides administrative functionalities for managing users and transactions.

# Modules

- Authentication: User registration, login, logout, and access control.
- Transaction Management: Viewing all transactions, making direct payments to other registered users.
- Payment Requests: Requesting payments from registered users, accepting, and canceling money requests.
- Admin Management: For admins, viewing all user accounts and balances, viewing all payment transactions, registering more administrators.
- Security: Implemented security measures including XSS, CSRF, SQL injection, and clickjacking protection.
- Web Services: Currency conversion service using external APIs and fallback hardcoded exchange rates.
- Thrift Integration: Timestamping transactions and money requests with Apache Thrift.
- Deployment: It was deployed on AWS.

# How to run the app
Run this command in project directory to install dependencies:

pip3 install -r requirements.txt

**To run with http**:

python manage.py runserver

**To run with https**:

python manage.py runserver_plus --cert-file domain_name.crt --key-file domain_name.key

# Some screenshots from the app

<img width="468" alt="image" src="https://github.com/makisacik/django-online-payment-app/assets/71513921/09dce887-132d-42b5-a25e-4fe12a38c470">

<img width="468" alt="image" src="https://github.com/makisacik/django-online-payment-app/assets/71513921/21c609c6-bb9e-49fd-b4a6-4e99012e21a1">

<img width="468" alt="image" src="https://github.com/makisacik/django-online-payment-app/assets/71513921/3b773ce5-f7b1-4324-9c1e-634162fd115c">

<img width="468" alt="image" src="https://github.com/makisacik/django-online-payment-app/assets/71513921/65b0dfcc-9068-4838-9200-158caf0c5d74">

<img width="468" alt="image" src="https://github.com/makisacik/django-online-payment-app/assets/71513921/4fa7a827-5905-4314-a3cd-6920778e8bc1">

<img width="468" alt="image" src="https://github.com/makisacik/django-online-payment-app/assets/71513921/2d165022-ae18-4b55-864b-2c406f6b2e42">
