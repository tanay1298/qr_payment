Binance Trade Monitoring
==========

### Tech Stack
- `django` version 5.0.3 - [documentation](https://docs.djangoproject.com/en)
- `python` version 3.10.4

### Maintaining requirements

`requirements.txt`

### Structure:
- Each app has its own directory.
- Within qr_payment:
  - settings.py: All global configurations

Local setup
===========
- Clone repository

```bash
git@github.com:tanay1298/qr_payment.git
```
- For `settings_local.py`
  - set `DEBUG=True` if not set, for all loggings on console


```bash
# install virtual environment
pip install --user virtualenv

# create virtual environment 
virtualenv -p /usr/bin/python venv

# activate virtual environment
# make sure venv folder is in current folder
source venv/bin/activate

# Now whenever you install any package will be insalled in venv folder

# Now install all the dependencies
pip install -r requirements.txt

# Now you can start server
# replace 3000 for desired port
python manage.py runserver 0.0.0.0:3000
```

```bash
# Some commands for debugging
# make sure virtualenv is activated

# Open django shell
python manage.py shell

# While development, when any model is modified
python manage.py makemigrations

# reflect changes to database
python manage.py migrate

# To deactivate virtualenv
deactivate

```

Database Design Documentation:
=========
[db_design](db_design.md)


Technical Overview
=======

1. Create order by Customer

```bash
/create-order/
```

2. Generate QR Code by merchant to receive payment

```bash
generate-qr-code/
```

3. Payment processing by Customer

```bash
process-payment/
```

Logging:
========
When `DEBUG=True`, all logs will go to console irrespective of any environments

### Log Levels
 
- DEBUG: Low level system information for debugging purposes
- INFO: General system information
- WARNING: Information describing a minor problem that has occurred.
- ERROR: Information describing a major problem that has occurred.
- CRITICAL: Information describing a problem needed an attention