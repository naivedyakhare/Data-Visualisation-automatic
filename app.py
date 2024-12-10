#####################################################################################################################
from openai import OpenAI
import streamlit as st
import pyreadstat
#####################################################################################################################

def get_prompt_history():
    prompt = [
        '''You are a Data Analyst that generates r code.''',
        '''You will be given a query. Based on that query, you will generate python code for Data Visualisaton.
1. You will be given dataset path and dataset name for the dataset that will be used for visualisation
2. You will be given metadata of the dataset for reference to generate visualisation based on, which contains the column names and their corresponding labels.
3. You will only give code, no need for any kind of explanation.
4. You will be given more stuff, keep that in mind while writing the code.
5. The dataset will in sas7bdat.
6. Do not use triple backticks or any syntax highlighting; just return plain text code'''
    ]

    return prompt
#####################################################################################################################

def generate_prompt_from_query(user_query, dataset_path, dataset_name, metadata):

    prompt = f'''
# User Query
{user_query}

# Dataset Metadata
{metadata}

# Dataset Location
File Absolute Path - {dataset_path}
File Name - {dataset_name}

# Insturctions
Follow these instructions:
    1. Generate Python code based on the query.
    2. No explaination, only code with no prefixes or suffixes.
    3. Do not use triple backticks or any syntax highlighting; just return plain text code.
    4. Use pyreadstat to read sas7bdat files.
    5. Use Plotly to create interactive graphs.
    6. Separate the categorical variable by different colours, ALWAYS.
    7. Also, save the graph in the local storage.

'''
    
    return prompt
#####################################################################################################################

def get_dataset_metadata(dataset_path, dataset_name):
    if dataset_path != "":
        file_path = f"{dataset_path}/{dataset_name}"
    else:
        file_path = f"{dataset_name}"

    file_ext = dataset_name.split(".")[1]
    if file_ext == "sas7bdat":
        df, meta = pyreadstat.read_sas7bdat(file_path)
    elif file_ext == "xpt":
        df, meta = pyreadstat.read_xport(file_path)
    elif file_ext == "xlsx":
        df, meta = pyreadstat.read_xport()



    return meta.column_names_to_labels

#####################################################################################################################

def generate_messages_openai(user_query, dataset_path, dataset_name, metadata):
    
    previous_prompts = get_prompt_history()
    user_prompt = generate_prompt_from_query(user_query, dataset_path, dataset_name, metadata)

    messages = []
    for prompt in previous_prompts:
        messages.append({"role":"user", "content": prompt})
    messages.append({"role":"user", "content": user_prompt})

    return messages
#####################################################################################################################

def call_openai(api_key, messages):

    client = OpenAI(api_key = api_key)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )

    return response.choices[0].message.content
#####################################################################################################################

def generator(api_key, user_query, dataset_path, dataset_name):
    metadata = get_dataset_metadata(dataset_path, dataset_name)
    st.write(dataset_name, dataset_path)
    messages = generate_messages_openai(user_query, dataset_path, dataset_name, metadata)
    response = call_openai(api_key, messages)

    return response
#####################################################################################################################

# Sidebar for API Key, File Inputs, and Dataset Name
st.sidebar.header("Configuration")
api_key = st.sidebar.text_input("Enter your OpenAI API Key", type="password")
dataset_path = st.sidebar.text_input("Enter the File Path", value ="")
dataset_name = st.sidebar.text_input("Enter the Dataset Name", value="bmi.xpt")

# Query Input
user_query = st.text_area("Enter your query for visualization (e.g., 'Generate a bar chart of sales over time'): ")


if st.button("Generate Visualization"):
    if api_key and dataset_path and dataset_name and user_query:
        try:
            # Generate Python code for visualization using OpenAI
            st.write("Generating code for visualization...")

            generated_code = generator(api_key, user_query, dataset_path, dataset_name)

            # Display the generated code (for user review)
            st.code(generated_code, language="python")

            # Execute the generated code
            try:
                # Redirect stdout to capture any print statements from the code execution
                exec(generated_code)
              
            except Exception as e:
                st.error(f"An error occurred while executing the generated code: {e}")
        except Exception as e:
            st.error(f"An error occurred while loading the dataset: {e}")
    else:
        st.warning("Please make sure to fill in all fields (API Key, File Path, Dataset Name, and Query) before generating.")
