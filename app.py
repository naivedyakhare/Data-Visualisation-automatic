#####################################################################################################################
from openai import OpenAI
import streamlit as st
import pyreadstat
import os
from dotenv import load_dotenv
load_dotenv()
#####################################################################################################################

styl = """
<style>
    .stTextArea {
      position: fixed;
      bottom: 4rem;
    }
    .stButton {
      position: fixed;
      bottom: 1rem;
      display: flex;
      justify-content: flex-end;
    }
    .stMain .stMainBlockContainer {
        width: 140%;
    }
    .stMainBlockContainer *{
        width: 140%;
    }
    .stVerticalBlock {
    }
</style>
"""


# Initialize session state for chat
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    st.session_state.chat_display_history = [{"message": "Type in a query and hit send to generate", "is_user": False}]
    st.session_state.response = ["Enter your queries and I will generate graph for you!"]
    st.session_state.chat_length = 0

# Initialising chat container
chat_placeholder = st.empty()

# Initial Chat History
prompt = [
    '''You are a Data Analyst that generates Python code for Data Visualization.''',
    '''A user will chat with you giving you queries. Based on those queries, you will generate Python code for Data Visualization.
1. You will be given dataset path and dataset name for the dataset that will be used for visualization.
2. You will be given metadata of the dataset for reference to generate visualization based on, which contains the column names and their corresponding labels.
3. You will only give code, no need for any kind of explanation.
4. The dataset will be in SAS7BDAT or XPT format.
5. Do not use triple backticks or any syntax highlighting; just return plain text code.''',
]
st.session_state.chat_history.append({"role": "system", "content": prompt[0]})
st.session_state.chat_history.append({"role": "user", "content": prompt[1]})

#####################################################################################################################
# Helper Functions

def generate_prompt_from_file_spec(user_query, dataset_path, dataset_name, output_file_name):
    metadata = get_dataset_metadata(dataset_path, dataset_name)
    prompt = f'''
# Dataset Metadata
{metadata}

# User Query
{user_query}

# Dataset Location
File Absolute Path - {dataset_path}
File Name - {dataset_name}
Output File Name = {output_file_name}

# Instructions
1. Generate Python code based on the query.
2. No explanation, only code with no prefixes or suffixes.
3. Do not use triple backticks or any syntax highlighting; just return plain text code.
4. Use pyreadstat to read SAS7BDAT or XPT files.
5. Use Plotly to create interactive graphs.
6. Separate the categorical variables/Group by variables by different colors (e.g., green, red, blue).
7. Save the graph as an HTML file in the local storage.
8. Save the graph using - fig.write_html("graph.html", include_plotlyjs="cdn", full_html=True).
9. The dimensions of the graph should be these height=400, width=670! It's really important
'''

    return prompt
#####################################################################################################################

def get_dataset_metadata(dataset_path, dataset_name):
    try:
        file_path = f"{dataset_path}/{dataset_name}" if dataset_path != "." else dataset_name
        file_ext = dataset_name.split(".")[-1]

        if file_ext == "sas7bdat":
            _, meta = pyreadstat.read_sas7bdat(file_path)
        elif file_ext == "xpt":
            _, meta = pyreadstat.read_xport(file_path)
        else:
            raise ValueError("Unsupported file format. Please use a SAS7BDAT or XPT file.")

        return meta.column_names_to_labels
    except Exception as e:
        st.error(f"Failed to load metadata: {e}")
        return None
#####################################################################################################################

def generate_prompt(user_query, dataset_path, dataset_name, output_file_name):
    # Keeping count of chat length
    
    prompt_user_query = generate_prompt_from_file_spec(user_query, dataset_path, dataset_name, output_file_name)
    st.session_state.chat_history.append({"role": "user", "content": prompt_user_query})

    return st.session_state.chat_history
#####################################################################################################################

def call_openai(api_key, messages):
    try:
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=messages
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Failed to call OpenAI API: {e}")
        return None

#####################################################################################################################
# Main Generator Function

def generator(api_key, user_query, dataset_path, dataset_name, output_file_name):

    messages = generate_prompt(user_query, dataset_path, dataset_name, output_file_name)
    response = call_openai(api_key, messages)

    st.session_state.chat_history.append({"role": "assistant", "content": response})

    st.session_state.chat_length += 1
    return response

#####################################################################################################################
#####################################################################################################################
# Display Chat content here
AVATAR = "✨"
user_query = st.chat_input("Enter something")
#####################################################################################################################
#####################################################################################################################

# st.title("Interactive Data Visualization Generator")
# st.write("Start a conversation to generate visualizations interactively.")

# Sidebar for API Key and Dataset Inputs
st.sidebar.header("Configuration")
# api_key = st.sidebar.text_input("Enter your OpenAI API Key", type="password")
api_key = os.environ.get("OPENAI_API_KEY")
dataset_path = st.sidebar.text_input("Enter the File Path", value= r"C:\Users\rohit\OneDrive\Desktop\Medtek\Data Visualisation automatic - 2\adam\datasets", placeholder="Type . if no path")
dataset_name = st.sidebar.text_input("Enter the Dataset Name", value="advs.xpt", placeholder="e.g., dm.sas7bdat")
output_file_name = st.sidebar.text_input("Enter output file Name", value="graph")

# Chat UI

# Input box for user query


# Generate button
if user_query:
    if api_key and dataset_path and dataset_name and user_query:
        try:
            # Generate response from OpenAI
            # st.session_state.chat_display_history.append(user_query)
            generated_code = generator(api_key, user_query, dataset_path, dataset_name, output_file_name)
            st.session_state.chat_display_history.append({"message": user_query, "is_user": True, "key": f"user_query_{st.session_state.chat_length}"})

            if not generated_code:
                st.error("Failed to generate code. Check the logs or refine your query.")
            else:
                # Display the generated code
                # st.code(generated_code, language="python")

                # Save and execute the generated code
                with open("generated_code.py", "w", encoding="utf-8") as f:
                    f.write(generated_code)
                    f.close()
                    
                try:
                    # Execute the generated code
                    exec(generated_code, globals())

                    # Display the graph
                    if os.path.exists("graph.html"):
                        with open("graph.html", "r", encoding="utf-8") as f:
                            html_content = f.read()
                            # st.components.v1.html(html_content, height=400, width=670)
                            st.session_state.chat_display_history.append({"message": html_content, "is_user": False, "key": f"response_{st.session_state.chat_length}"})
                            
                            f.close()
                    else:
                        st.error("Graph file not found after code execution.")

                except Exception as e:
                    st.error(f"An error occurred while executing the generated code: {e}")
                
        except Exception as e:
            st.error(f"An error occurred while processing your request: {e}")
    else:
        st.warning("Please ensure all fields (API Key, File Path, Dataset Name, and Query) are filled before proceeding.")


for message in st.session_state.chat_display_history:
    if message["is_user"]:
        with st.chat_message("user"):
            st.markdown(message["message"] )
    else:
        with st.chat_message("assistant", avatar=AVATAR):
            st.components.v1.html(message["message"], height=400, width=670)