
import shutil
import os
import zipfile


class File:
    def __init__(self, path: str):
        self.path = path
        self.size = os.path.getsize(self.path)


class Folder:
    def __init__(self, directory: str):
        self.path = directory
        self.files = []
        self.size = 0
        self.maxed = False

    def add_file(self, file: File):
        self.new_size = file.size + self.size
        if self.new_size > 25000000:
            self.maxed = True
        if not self.maxed:
            self.files.append(file.path)
            self.size = self.size + file.size


class FolderMaker:
    def __init__(self, directory: str):
        self.file_directory = directory
        self.files = [f'{self.file_directory}\\{x}' for x in os.listdir(
            self.file_directory)]
        self.current_folder = Folder(f'{self.file_directory}\\zip0')
        self.folders = []
        self.folder_count = 0

    def new_folder(self):
        self.folders.append(self.current_folder)
        self.folder_count = self.folder_count + 1
        self.current_folder = Folder(
            directory=f'{self.file_directory}\\zip{self.folder_count}')

    def make(self):

        for file in self.files:
            self.current_file = File(file)
            if not self.current_folder.maxed:
                self.current_folder.add_file(self.current_file)
            else:
                self.new_folder()
                text = f'new folder {self.current_folder.path}'
                print(text)
                self.current_folder.add_file(self.current_file)

    def zip_up(self):
        for folder in self.folders:
            zip_file = str(folder.path).replace('/', '\\') + '.zip'
            with zipfile.ZipFile(zip_file, 'w') as my_zip:
                for file in folder.files:
                    name = str(file).split('//')[-1]
                    my_zip.write(filename=file, arcname=name)
                    print(f'zipping {file}')


def get_file():
    import PySimpleGUI as sg
    layout = [
        [sg.I("", key='PATH'), sg.FolderBrowse(key='Browser')],
        [sg.Submit()],
        [sg.Exit()]
    ]
    window = sg.Window("folder browse", layout=layout, finalize=True)
    retv = ""
    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            retv = None
            window.close()
            break
        if event == 'Browser':
            value = str(values['Browser'][0])
            print(value)
            window['PATH'].update(value)
            window.refresh()

        if event == 'Submit':
            if window['PATH'] != '':
                retv = str(values['PATH'])
                window.close()
                break
    print(retv)
    return retv


def main():
    folder = get_file()
    fmaker = FolderMaker(folder)
    fmaker.make()
    fmaker.zip_up()


if __name__ == '__main__':
    main()


#
# import zipfile
#
# zip_file_name = 'my_zip_file.zip'  # the name of the zip file you want to create
# file_to_zip = 'path/to/my/file.txt'  # the file you want to add to the zip file
#
# create a new zip file and open it in write mode
# with zipfile.ZipFile(zip_file_name, 'w') as my_zip:
#    # add the file to the zip file
#    my_zip.write(file_to_zip, arcname='file.txt')
