from keep_alive import keep_alive
import data

records = data.get('TEST')
records.append({'test': 'g', 'test1': 'h'})
records[1]['fsd'] = 'q'
print(records)
data.set('TEST', records)

keep_alive()