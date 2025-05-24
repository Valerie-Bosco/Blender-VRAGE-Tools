import os
import shutil


def main():

    src = os.path.join(os.path.dirname(__file__), 'vrage_tools')

    with open(os.path.join(src, '__init__.py')) as f:
        lines = f.read()
    f.close()

    version = lines[lines.find('"version" : (') + len('"version" : ('):]
    version = version[:version.find('),')].replace(', ', '.')

    target = os.path.join(os.path.dirname(__file__), f"vrage_tools_v{version}")

    shutil.copytree(src, os.path.join(os.path.dirname(__file__), 'temp', 'vrage_tools'))
    temp_folder = os.path.join(os.path.dirname(__file__), 'temp')

    zipfile = shutil.make_archive(target, 'zip', temp_folder)

    shutil.rmtree(temp_folder)


if __name__ == '__main__':
    main()