import os
import sys
import subprocess
import shutil
from setuptools import setup, find_packages
from setuptools.command.build_ext import build_ext
from Cython.Build import cythonize

class Build: 
    def __init__(self, config):
        """
        Constructor for the Build class.

        Parameters:
        - config (dict): Configuration dictionary for the build.
        """ 
 
        Build.run(config)
    @staticmethod
    def run(config):
        """
        Runs the build process based on the specified configurations.
        """
        # Retrieve args and config
        args = Build.init_args(sys.argv)  
        config['base'] = Build.get_base()
        #config['iwd'] = os.getcwd() # initial working directory

        if not os.path.isdir(config['base']):
            print('Base not found')
            sys.exit()
            
        # 
        os.chdir(config['base'])

        
        # Act in consequence
        # help
        if "--help" in args:
            Build.show_help()   
            sys.exit()
        # if none then it's all 
        if '--exe' not in args and '--pyd' not in args and '--pyc' not in args:
            args = args + ['--exe', '--pyd', '--pyc', '--remove-previous']
        print('RUNNING UPBT:',config['base'], args[1:])  
        
        # remove build and dist if -r
        if "--remove-previous" in args:
            r = Build.remove_prev()
        
        # run required stuff
        #try:
           
        if "--pyd" in args:
            r = Build.Builds.Pyd.run(config.get('pyd'))
            # if r.get('error'): raise Exception 
        if "--pyc" in args:
            r = Build.Builds.Pyc.run(config.get('pyc'))
            # if r.get('error'): raise Exception 
        if "--exe" in args:
            r = Build.Builds.Exe.run(config.get('exe'))
                # if r.get('error'): raise Exception 
        #except Exception as e:
        #    print(e)

        
        print('UPBT FINISHED') 

    @staticmethod
    def run_subprocess(command_lines):
        """
        Runs a subprocess with the provided command lines.

        Parameters:
        - command_lines (str or list): Command lines to execute.

        Returns:
        - dict: Result of the subprocess execution.
        """
        if isinstance(command_lines, str):
            command_lines = command_lines.split("&&")

        for command in command_lines:
            # Run the command and capture the output
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True, 
            )

            for line in process.stdout:
                print(f"{line}", end='', flush=True)

            for line in process.stderr:
                print(f"{line}", end='', flush=True)

            # Wait for the command to complete
            process.wait()

            # Check if the command was successful
            if process.returncode != 0:
                return {'error': True, 'code': process.returncode, 'stderr': str(process.stderr), 'command': command}
            
            return {'code': 'RunSubprocessSuccess', 'error': False}

    @staticmethod
    def init_args(args):
        """
        Initializes command-line arguments, converting shorthand options to their long forms.

        Parameters:
        - args (list): List of command-line arguments.

        Returns:
        - list: Modified list of command-line arguments.
        """
        if '-h' in args:
            sys.argv[sys.argv.index("-h")] = '--help'
        if '-r' in args:
            sys.argv[sys.argv.index("-r")] = '--remove-previous'
        if '-e' in args:
            sys.argv[sys.argv.index("-e")] = '--exe'
        if '-c' in args:
            sys.argv[sys.argv.index("-c")] = '--pyc'
        if '-d' in args:
            sys.argv[sys.argv.index("-d")] = '--pyd'
        
        return args

    @staticmethod
    def get_base():
        """
        Get base folder (first argument (1))
        If first argument does not start by - it will interpret it as base
        """
        if len(sys.argv)>1:
            if not sys.argv[1].startswith('-'):
                base = sys.argv[1]
                del sys.argv[1]
                return base
        return '.'    
            

    @staticmethod
    def remove_prev():
        """
        Removes the 'build' and 'dist' directories if the --remove-previous option is present.
        """
        if "--remove-previous" in sys.argv:
            del sys.argv[sys.argv.index("--remove-previous")]
        if os.path.exists('build'):
            shutil.rmtree('build')
        if os.path.exists('dist'):
            shutil.rmtree('dist')

    @staticmethod
    def show_help():
        """
        Displays help information and exits the script.
        """
        print('UBPT help')
        print('- `-h,--help` : Display help information.')
        print('- `-r,--remove-previous` : Remove the "build" and "dist" directories before building.')
        print('- `-e,--exe` : Build the executable using pyinstaller.')
        print('- `-d,--pyd` : Build Python extension modules (pyd) using Cython.')
        print('- `-c,--pyc` : Build Python wheels (pyc) using pip.')
        

    class Builds: 
   
            
        class Pyd:
            @staticmethod
            def run(config):
                options = config.get('options',)
           
                """
                Builds a Python extension module (pyd) using Cython.

                Parameters:
                - config (dict): Configuration dictionary for the pyd build.
                """
                input = config.get('input','')
                # build pyd
                if "--pyd" in sys.argv:
                    del sys.argv[sys.argv.index("--pyd")]
            
                print('Building inplace pyd compilation...')
                additional_params = ["build_ext", "--inplace"]
                # deprecated: f"--build-lib={os.path.join(base,'build')}",f"--build-temp={os.path.join(base,'build')}
                if options and len(options)>0: additional_params.append(options)

                py_files = Build.Builds.Pyd.find_py_files(f'{input}')
                ext_modules = Build.Builds.Pyd.create_extension_modules(py_files)

                setup(
                    ext_modules=ext_modules,
                    script_args=additional_params, 
                    # Other setup configuration...
                )

                return {'code': 'BuilderPydBuilt', 'updated': True}


            @staticmethod
            def find_py_files(directory):
                """
                Finds Python files in the specified directory, excluding those starting with '__'.

                Parameters:
                - directory (str): Directory to search for Python files.

                Returns:
                - list: List of Python files found.
                """
                py_files = []
                for root, dirs, files in os.walk(directory):
                    # Exclude directories starting with __
                    dirs[:] = [d for d in dirs if not d.startswith('__')]
                    
                    for file in files:
                        if file.endswith(".py") and not file.startswith('__init__'):
                            py_files.append(os.path.join(root, file))
                return py_files

            @staticmethod
            def create_extension_modules(py_files):
                """
                Creates Cython extension modules from the specified Python files.

                Parameters:
                - py_files (list): List of Python files to convert.

                Returns:
                - list: Cython extension modules.
                """
               
                ext_modules = cythonize(py_files)
            
                return ext_modules

        class Pyc:
            @staticmethod
            def run(config):
                """
                Builds a Python wheel (pyc) using pip wheel.

                Parameters: 
                - config (dict): Configuration dictionary for the wheel build.
                """
                # build pyc
                if "--pyc" in sys.argv:
                    del sys.argv[sys.argv.index("--pyc")]
                
                input = config.get('input', '.')
                output = config.get('output', 'dist')
                name = config.get('name', 'UnnamedPackage')
                version = config.get('version', '1.0.0')
                options = config.get('options', '')
                print(f'Building wheel on {output}')
                r = Build.run_subprocess(f'pip wheel --no-deps -w {output} {input}')  # instead of DEPRECATED:'python setup.py bdist_wheel',
                if r.get('error'):
                    return r
                print('(Re)installing library...')
                r = Build.run_subprocess(f'pip install {output}/{name}-{version}-py3-none-any.whl {options}')
                if r.get('error'):
                    return r
                
                return {'code': 'BuilderPycBuilt', 'updated': True}


        class Exe:
            @staticmethod
            def run(config):
                """
                Builds an executable (exe) using PyInstaller and copies the .env file if it exists.

                Parameters: 
                - config (dict): Configuration dictionary for the exe build.

                Returns:
                - dict: Result of the exe build.
                """
                input = config.get('input')
                output = config.get('output', 'dist')
                options = config.get('options', '')
                # Set the output
                if '--dispatch' not in options:
                    options = options + f' --distpath {output}' 
                
                # build exe
                if "--exe" in sys.argv:
                    del sys.argv[sys.argv.index("--exe")]
                print(f'Building exe at {os.getcwd()}')
                r = Build.run_subprocess(f'pyinstaller {input} {options}') 
                if r.get('error'):
                    return r
                try: 
                    if os.path.exists('.env'):
                        shutil.copy('.env', f'{output}/.env')
                except Exception as e:
                    return {'code': 'BuilderEnvException', 'error': True}

                return {'code': 'BuilderExeBuilt', 'updated': True}
