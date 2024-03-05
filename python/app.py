import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json
import xml.etree.ElementTree as etree
import os

def load_data(file_format):
    try:
        if file_format == "csv":
            return pd.read_csv("data.csv").to_dict(orient="records")
        elif file_format == "json":
            with open("data.json", "r") as f:
                return json.load(f)
        elif file_format == "xml":
            tree = etree.parse("data.xml")
            root = tree.getroot()
            data = [
                {
                    "name": root[i].find("name").text,
                    "age": int(root[i].find("age").text),
                    "address": root[i].find("address").text,
                }
                for i in range(len(root))
            ]
            return data
    except FileNotFoundError:
        return None
    except Exception as e:
        st.error(f"Error occurred: {str(e)}")

def save_data(name, age, address, file_format, save_folder="data", filename="data"):
    try:
        data = {"name": name, "age": age, "address": address}
        if file_format == "csv":
            df = pd.DataFrame(data, index=[0])
            save_path = os.path.join(save_folder, filename + ".csv")
            df.to_csv(save_path, index=False)
        elif file_format == "json":
            with open(os.path.join(save_folder, filename + ".json"), "w") as f:
                json.dump(data, f)
        elif file_format == "xml":
            root = etree.Element("data")
            name_element = etree.SubElement(root, "name")
            name_element.text = name
            age_element = etree.SubElement(root, "age")
            age_element.text = str(age)
            address_element = etree.SubElement(root, "address")
            address_element.text = address
            tree = etree.ElementTree(root)
            tree.write(os.path.join(save_folder, filename + ".xml"), encoding="utf-8", xml_declaration=True)
        st.success("Data saved successfully!")
    except Exception as e:
        st.error(f"Error occurred while saving data: {str(e)}")

def show_data(data):
    if data:
        st.subheader("Loaded Data:")
        st.write(pd.DataFrame(data))
    else:
        st.info("No data loaded yet.")

def plot_data(data):
    if data:
        df = pd.DataFrame(data)
        name_counts = df['name'].value_counts()

        # Create bar chart
        plt.figure(figsize=(8, 6))
        name_counts.plot(kind='bar')
        plt.xlabel("Name")
        plt.ylabel("Number of entries")
        plt.title("Number of Entries by Name (Bar Chart)")
        plt.xticks(rotation=45, ha="right")
        st.pyplot()

        # Create pie chart
        plt.figure(figsize=(6, 6))
        name_counts.plot(kind='pie', autopct="%1.1f%%")
        plt.title("Number of Entries by Name (Pie Chart)")
        st.pyplot()
    else:
        st.info("No data saved yet.")

st.title("Data Collection and Display App")

# Collect user input
name = st.text_input("Name:")
age = st.number_input("Age:", min_value=0)
address = st.text_input("Address:")

# Select file format for saving
file_format = st.selectbox("Select file format:", ["csv", "json", "xml"])

# Define loaded_data variable
loaded_data = None

# Button to save data
if st.button("Save Data"):
    save_data(name, age, address, file_format)

# Button to display data
if st.button("Display Data"):
    loaded_data = load_data(file_format)
    show_data(loaded_data)

# Button to plot data
if st.button("Plot Data"):
    plot_data(loaded_data)
