# Index

1. [Universal Package Building Tool (UPBT)](#universal-package-building-tool-upbt)
2. [Usage](#usage)
   - [Clone the Repository](#1-clone-the-repository)
   - [Create a `build.py` File](#2-create-a-buildpy-file)
   - [Run the Script](#4-run-it-when-required)
3. [Command-line Arguments](#command-line-arguments)
4. [Configuration](#configuration)
5. [License](#license)
6. [Development Notes](#development-notes)
   - [TODO](#todo)
   - [Rebuild UPBT and Install](#rebuild-upbt-and-install)
7. [End](#end)

# Universal Package Building Tool  

This Python script provides a flexible build system for your project. It supports building executables (exe), Python extension modules (pyd), and Python wheels (pyc). The script uses PyInstaller for exe builds, Cython for pyd builds, and pip for wheel builds.
Easyly expandable for ones own needs. Feel free.

## Usage

1. Install upbt (if not installed already):
   ```bash
   git clone https://github.com/iorp/upbt.git  Unpublished yet,see [Development Notes](#development-notes).
   pip install iorp@upbt --force-reinstall --no-deps Unpublished yet,see [Development Notes](#development-notes).
   pip install dist/upbt --force-reinstall --no-deps
   ```
  
3. Create a build.py file in your project root, with setup.py

build.py
```python
     
from upbt.builder import Build
 
builderConfig={  
        'pyd':{
            'target':'./mylibrary'
        },
        'pyc':{
           
            #'input':'.', # optional, default value
            #'output':'dist', # optional, default value
            #'version':'1.0.0', # optional, default value # it must be the same as setup.py
            'name':'mylibrary', # The package name
            'options':'--force-reinstall' # Optional. Any other pip install options 

        },
        'exe':{
            'input':'__main__.py', # the input file name 
            #'output':'dist', # optional, default value
            'options':'--onefile --name e' # Optional. Any other pyinstaller options the output file name goes here
            
        }
 
}

#call the build class
Build(builderConfig) 

```
4. Run it when required 
```shell
python build.py [options]
```

### Command-line Arguments

Note that if no options are provided it will put all (excepting hep)

- `-h,--help` : Display help information.
- `-r,--remove-previous` : Remove the 'build' and 'dist' directories before building.
- `-e,--exe` : Build the executable using PyInstaller.
- `-d,--pyd` : Build Python extension modules (pyd) using Cython.
- `-c,--pyc` : Build Python wheels (pyc) using pip.

### Configuration

The script reads configurations from a dictionary specified in the script. Modify the `config` dictionary in the script to customize the build settings.

```python
config = {
    'exe': {
        'input': 'your_script.py',
        'output': 'dist',
        'options': '--additional-options',
    },
    'pyd': {
        'target': 'your_package',
    },
    'pyc': {
        'input': 'your_package',
        'output': 'dist',
        'name': 'YourPackageName',
        'version': '1.0.0',
        'options': '--additional-options',
    },
} 

```


## License

This project is licensed under the [MIT License](LICENSE).
 

Feel free to customize the README to better fit your project's structure and documentation needs.


 

# Development notes

# TODO 
- Relativize running options names ( exe, pyd, pyc) 
- no build if no config


# ReBuild UPBT and Install:

In the root directory of UPBT package, run the following command to build a distribution package:
This will create a dist directory with a .tar.gz file,and reinstall

```bash 
python setup.py sdist  
pip install dist/upbt-1.0.0.tar.gz --force-reinstall --no-deps

```
 
