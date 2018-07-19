# Windows

## Installation
1. Download Python 3.6 ([link](https://www.python.org/downloads/windows/))
1. Open CMD
   - Press `Win` + `R`
   - Type in: `cmd.exe`
1. Download project from GitHub
1. Unpack it
1. Move to project folder in CMD
   - Type in: `cd /d C:\project_folder`
   - `project_folder` is just a template
   - Enter real path where you unpacked project, e.g. `cd /d D:\shops-scraper-master`
1. Install virtual environment, type in: 
   - `virtualenv venv`
   - `venv\Scripts\activate`
1. Install Microsoft Build Tools ([link](https://www.microsoft.com/en-us/download/details.aspx?id=48159&ranMID=24542&ranEAID=je6NUbpObpQ&ranSiteID=je6NUbpObpQ-ssahJLOBHslxW96rArFYOQ&epi=je6NUbpObpQ-ssahJLOBHslxW96rArFYOQ&irgwc=1&OCID=AID681541_aff_7593_1243925&tduid=(ir_w8F3Uex8PV0Mzu7UEdzN2ycQUkjVBxU5XxduzU0)(7593)(1243925)(je6NUbpObpQ-ssahJLOBHslxW96rArFYOQ)()&irclickid=w8F3Uex8PV0Mzu7UEdzN2ycQUkjVBxU5XxduzU0))
1. Install project's dependencies. In CMD type in:
   - `pip install -r requirements.txt`
   - Check output carefully, there have to be **no errors**, all commands have to be executed **succesfully**
   - Installation will take a while

## Launch
1. Open CMD
1. Move to project folder
1. Activate virtual environment
   - `venv\Scripts\activate`
1. Move to `shops` directory
   - `cd /d shops`
1. Run script
   - `python3 run.py`
1. Scraping will take a couple of hours
1. When scraping is done `Bags.xlsx` will be updated with a new data
