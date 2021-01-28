from test_planeks.celery import app
from .csv_generator import generate_row
import io, csv
from django.core.files import File
from .models import Dataset


@app.task
def write_csv(config, rows, dataset_id):
    dataset = Dataset.objects.get(pk=dataset_id)
    buffer_texted = io.StringIO()
    writer = csv.writer(buffer_texted,
                        delimiter=config['delimiter'],
                        quoting=csv.QUOTE_ALL,
                        quotechar=config['quote'])
    writer.writerow(config['fieldnames'])
    for row in range(rows):
        writer.writerow(generate_row(config))
    buffer_binary = io.BytesIO(buffer_texted.getvalue().encode('utf-8'))
    file = File(buffer_binary)
    path = f'{config["name"]}_{dataset.id}.csv'
    dataset.file.save(path, file)
    dataset.status = True
    dataset.save()

