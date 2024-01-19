# 3ds Max Auto reloader

Simple script to watch a folder for changes and auto reload and imported modules in 3ds Max. Requires [watchfiles](https://github.com/samuelcolvin/watchfiles) to be installed in your 3ds Max environment. Only tested in 3ds Max 2024 and with pure Python solutions.

**Important!** Does not work if you run any pymxs code on reload since the reload code runs in its own thread.

## How to
* Open cmd and run the following commands
    * "C:\Program Files\Autodesk\3ds Max 2024\Python\python.exe" -m ensurepip
    * "C:\Program Files\Autodesk\3ds Max 2024\Python\python.exe" -m pip install watchfiles
* Start 3ds Max 2024
* Run main.py
* Click the button to select what folder to watch for changes
