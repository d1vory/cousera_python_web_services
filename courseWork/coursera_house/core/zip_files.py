import os
from zipfile import ZipFile

files = os.listdir('./')

archive = 'att_23.zip'

with ZipFile(archive,'w') as zip:
    for file in files:
        if file.endswith('.py'):
            zip.write(file)

print('All files zipped successfully!')

