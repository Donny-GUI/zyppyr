import zipfile
import os

CWD = os.getcwd()
print(CWD)


zip_paths = [f'{CWD}\\{x}' for x in os.listdir(CWD) if x.endswith('.zip')]
for z in zip_paths:
    print(z)
zip_home = f'{CWD}\\images'

passed = []
failed = []


def unzip_all(zips=zip_paths):
    for path in zips:
        zip_file = zipfile.ZipFile(file=path, mode='r')
        print(f'unzipping {path}')
        try:
            zip_file.extractall(zip_home)
            passed.append(path)
            zip_file.close()
        except:
            failed.append(path)
            zip_file.close()
    for index, path in enumerate(passed):
        os.remove(path)
    passed = []
    if failed != []:
        new_failed = failed
        failed = []
        unzip_all(new_failed)


if __name__ == '__main__':
    unzip_all()

