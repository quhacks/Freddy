import gspread, base64, os

sizes = {}

with open('auth.json', 'w', encoding='utf-8') as f: 
    f.write(base64.b64decode(os.getenv('AUTH')).decode('utf-8'))
client = gspread.service_account('auth.json')
os.remove('auth.json')
sheet = client.open_by_key(os.getenv('SHEET'))

def get(name):
    records = sheet.worksheet(name).get_all_records(numericise_ignore=['all'])
    sizes[name] = len(records)
    return records

def set(name, records, header=None):
    global sizes
    header = header or list(records[0].keys())
    size = sizes[name] if name in sizes else 0
    cells = [header]
    if name in sizes:
        cells += [['' for i in range(len(header))] for i in range(sizes[name])]
    size = 0

    for record in records:
        size += 1
        if size == len(cells):
            cells.append([''] * len(header))
        for key, value in record.items():
            if key in header:
                cells[size][header.index(key)] = value
                
    sizes[name] = size
    sheet.worksheet(name).update(cells)