# Query Recommendation System
To be filled later ...

# Data generation
The data needed to run the system is already provided.
In the situation in which the users wants to generate different datasets he will have to make sure to be located in the querryrec folder in his PC and then run `python .\src\datagen\datagenerator.py` for windows or `python ./src/datagen/datagenerator.py` for linux.

These commands will generate three different sizes of datasets, currently the size is static.

# What's in the coded folders
the `src` folder contains two folders, one for the data generation and one for the actual implementation of the system called `data setup`.
In the data setup folder are situated three `.ipynb` files that go step by step in the application.
The `query_recommendation.ipynb` notebook takes into account only the baseline as it uses only the smallest database data.
The `query_recommendation_evaluation.ipynb` is the main notebook to use when running the entire system as it uses all the datasets.
The `general_utility.ipynb` notebook is devoted to the execution of the part B of the project as it shows how our idea of utility could be implemented, since the main purpose was to show how well the approach we chose for the utility could work, the notebook uses only the baseline dataset.

# How to run the notebooks
The easiest way to run these notebooks would be by utilizing a jupyter notebook which allows to visualize different blocks of code and run each one separately, to properly work the blocks have to be run in order.
To install jupyter notebook simply run `pip install notebook` and to run it use `jupyter notebook`.
for more information on how to install, check out the [jupyter website](https://jupyter.org/install)

Another possible way to be able to run these files is through Visual Studio Code using the Jupyter extension that found in the extensions side of VScode, this will allow to correctly view the file and simply be able to click on the play button of each code block to run it or use the `run all` button on the top to automatically have the notebook run all the blocks in order and showing the results.



