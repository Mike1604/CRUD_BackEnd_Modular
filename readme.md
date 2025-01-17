# Backend Crud Modular
This folder includes the backend related to all the CRUDs of the project.

It uses python and FastApi to run the server.

### Running it locally
To run this in your local environment you will need first create a conda environment to handle all the dependencies. For this you will need to install conda and run the following command inside the project:

```
conda env create -f environment.yml
```
This will install all the dependencies and the conda environment so you can run it without any problems. 
After installation run the following command in the terminal to activate the conda environment
```
conda activate modular-crud-backend
```
Now you should be ready to start the app.
The app uses uvicorn to run the fastapi server, run the following command:
```

uvicorn app:app --reload --port 8001

```

This should create you a local server in port 8000 with the server running.


To check API docs you can go to
[API doc](http://127.0.0.1:8000/docs)

### In case of adding new dependencies
If you add new dependencies make sure to update the environment.yml file by running this command:
```
conda env export > environment.yml
```