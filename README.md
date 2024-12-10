# Auto Data Visualizer

Visualize data using Natural Language.

## Installation Guide

⚠️ You need to have python installed on your system

1. Getting the files ready

   - If you do not have git installed, simply go to the repository and download the zip file and then extract it wherever you want.
     ![alt text]({6B9C882F-C4A3-40B7-8CBC-85771AB1B80D}.png)

   - If you have git installed, clone the repository using the following command

     ```
     git clone https://github.com/naivedyakhare/Data-Visualisation-automatic
     ```

   Now open the downloaded/extracted folder in text editor or IDE of your choice.

2. (Optional) Create a Virutal Environment using conda or PIP
   - To create the environment
     ```
     conda create -p venv/
     ```
   - To activate the Environment
     ```
     conda activate venv/
     ```
3. Install the required packages in the requirements.txt
   ```
   pip install -r requirements.txt
   ```
4. After installation, simply run the following command
   ```
   streamlit run app.py
   ```
   The following command will open a browser window with a streamlit generated front-end where you have to enter some details.

## Generating Visualization

1. Folder Structure

   - `app.py` should be in the root folder.
   - The `dataset path` should be kept without the name of the dataset.
   - The visualization will be saved on the `root folder` itself.

2. Run the code using the following command in the commandline
   ```
   streamlit run app.py
   ```
3. Once the application is up and running, enter all the required details

   - OpenAI API key (required)
   - Dataset Path: If the dataset is in root folder type `.` (Do not leave empty)
   - Dataset Name (required): Name of the dataset including the extension. (Eg. DM.sas7bdat or bmi.xpt)
   - Visualization Query (required): Query for which you want to generate the visualisation for.

4. After entering all the details, click `Generatge Visualization` button.
5. The visualization will be generated below the button. Since this uses OpenAI (LLM) to generate graphs, it is prone to error and might sometimes not work.

## Working

Assuming the user has entered all the values correct

1. The code first checks if all the inputs are entered or not.
2. Then, it extracts the `metadata` (Column Names and their corresponding labels) from the dataset (for XPT and SAS7BDAT).
3. Then, it create a `prompt` that consists of the User's query, `metadata` and additional information.
4. The prompt that is created is sent to the OpenAI and it returns a Python code.
5. After the code is generated, it is directly run using the `exec` command, which (if errorless) is either displayed below the screen, or redirects to another webpage with an interactive graph.
