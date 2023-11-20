 

from upbt.builder import Build
  
Build({
 
        'pyd':{
            'input':'mylibrary',
            'options':'' # Optional. Any other setuptools setup() options
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
            'options':'--onefile --name mylibraryexe' # Optional. Any other pyinstaller options the output file name goes here, except --distpath
            
        }
 
})
        


