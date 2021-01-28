import random
import string
import sys


def generate_full_name():
    name_len = random.randint(4, 15)
    surname_len = random.randint(4, 15)
    name = ''.join(random.choice(string.ascii_lowercase) for _ in range(name_len)).capitalize()
    surname = ''.join(random.choice(string.ascii_lowercase) for _ in range(surname_len)).capitalize()
    return f'{name} {surname}'


def generate_job():
    job_list = ['veterinarian', 'actress', 'actor', 'architect',
                'singer', 'dentist', 'detective', 'writer', 'farmer',
                'nurse', 'pilot', 'engineer', 'accountant', 'butcher',
                'cashier', 'barber', 'carpenter', 'lifeguard', 'baker',
                'electrician', 'flight attendant', 'plumber', 'receptionist',
                'researcher', 'scientist', 'lawyer', 'bus driver', 'designer',
                'journalist', 'photographer', 'musician', 'painter', 'florist',
                'sales assistant', 'mechanic', 'model', 'shop assistant',
                'politician', 'translator', 'postman', 'hairdresser',
                'taxi driver', 'pharmacist', 'nanny', 'travel agent', 'cleaner',
                'biologist', 'businesswoman', 'businessman', 'dancer', 'gardener',
                'meteorologist', 'programmer', 'travel guide',
                'saleswoman', 'salesman']
    return random.choice(job_list)


def generate_email():
    extensions = ['com', 'net', 'org', 'gov', 'ua', 'com.ua']
    domains = ['gmail', 'yahoo', 'i', 'meta', 'bigmir', 'hotmail', 'post']
    extension = extensions[random.randint(0, len(extensions) - 1)]
    domain = domains[random.randint(0, len(domains) - 1)]
    account_len = random.randint(1, 20)
    account = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(account_len))
    e_mail = f'{account}@{domain}.{extension}'
    return e_mail


def generate_company_name():
    name_len = random.randint(3,15)
    name = ''.join(random.choice(string.ascii_lowercase) for _ in range(name_len)).capitalize()
    extensions = ['LLC', 'Inc', 'Co', 'Corp', 'Ltd']
    extension = random.choice(extensions)
    return f'{name} {extension}'


def generate_int_field(range_from: int, range_to: int):
    return random.randint(range_from, range_to)


def generate_date():
    year = random.randint(2005, 2021)
    month = random.randint(1, 12)
    day = random.randint(1, 31)
    month = str(month) if month >= 10 else "0" + str(month)
    day = str(day) if day >= 10 else "0" + str(day)
    return f'{year}/{month}/{day}'


def generate_int(start, stop):
    return random.randint(start, stop)


def get_csv_config(model, schema_id):
    config = {}
    schema = model.objects.get(id=schema_id)
    config['name'] = schema.name
    config['delimiter'] = schema.column_separator
    config['quote'] = schema.string_character
    columns_list = schema.columns.all().order_by('order')
    config['columns'] = []
    config['fieldnames'] = []
    for column in columns_list:
        config['fieldnames'].append(column.name)
        config['columns'].append({
            'type': column.type,
            'range_from': column.range_from if column.range_from else 0,
            'range_to': column.range_to if column.range_to else sys.maxsize,
        })
    return config


def generate_row(config):
    func_dict = {
        'd': generate_date,
        'f_n': generate_full_name,
        'c_n': generate_company_name,
        'e': generate_email,
        'j': generate_job,
        'i': generate_int
        }
    columns = config['columns']
    row = []
    for column in columns:
        cell = func_dict.get(column['type'])
        cell = cell(column['range_from'], column['range_to']) \
            if column['type'] == 'i' else cell()
        row.append(cell)
    return row



