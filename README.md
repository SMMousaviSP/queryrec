# Query Recommendation System
This is a query recommendation system using Jaccard Similarity and collaborative filtering to recommend queries to users based on the previous rated queries. Also a solution is provided to rate a query generally for all users. This project was done as part of the course "Data Mining" at the University of Trento by [Seyed Mohammad Mousavi](https://github.com/SMMousaviSP) and [Omar Facchini](https://github.com/OmarFacchini). You can find the report of the project in the `report` folder or simply by clicking [here](report/Query_Recommendation_System.pdf).

## Managing the Environment and Dependencies
To start working, first install `virtualenv` with pip.
```bash
pip install virtualenv
```

Then create an empty virtual environment.
```bash
virtualenv .venv
```
Note that `.venv` is the name of the virtual environment directory, this
directory is omitted in the `.gitignore` file.

After creating the virtual environment, activate it.

UNIX based Operating Systems (GNU/Linux, macOS, etc.)
```bash
source .venv/bin/activate
```

Windows
```batch
.\venv\Scripts\activate
```

Now you can install the required python packages in the clean environment you
just created.
```bash
pip install -r requirements.txt
```

# Data generation
The data needed to run the system is already provided.
In the situation in which the users wants to generate different datasets they will have to make sure to be located in the queryrec folder in their PC and then run `python .\src\datagen\datagenerator.py` for windows or `python ./src/datagen/datagenerator.py` for linux.

These commands will generate three different sizes of datasets, currently the size is static.

# What is in the folders
the `src` folder contains two folders, one for the data generation and one for the actual implementation of the system called `dataSetup`.
In the `dataSetup` folder there are three `.ipynb` files that go step by step in the application.
The `query_recommendation.ipynb` notebook takes into account only the baseline as it uses only the smallest database data.
The `query_recommendation_evaluation.ipynb` is the main notebook to use when running the entire system as it uses all the datasets.
The `general_utility.ipynb` notebook is devoted to the execution of the part B of the project as it shows how our idea of utility could be implemented, since the main purpose was to show how well the approach we chose for the utility could work, the notebook uses only the baseline dataset.

# How to run the notebooks
The easiest way to run these notebooks would be by utilizing a jupyter notebook which allows to visualize different blocks of code and run each one separately, to properly work, the blocks have to be run in order.
To install jupyter notebook simply run `pip install jupyterlab` and to run it use `jupyter lab` command.
for more information on how to install, check out the [jupyter website](https://jupyter.org/install)

Another possible way to be able to run these files is through Visual Studio Code using the Jupyter extension which can be found in the extensions side of this editor.
