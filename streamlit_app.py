import streamlit as st
import pyjsparser
import jsmin
import random
import string

def generate_random_string(length=8):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))

def obfuscate_code(js_code):
    # Parse the JavaScript code
    parser = pyjsparser.PyJsParser()
    parsed_code = parser.parse(js_code)
    
    # A dictionary to keep track of obfuscated variable names
    variable_map = {}

    def obfuscate_node(node):
        if isinstance(node, dict):
            if node.get('type') == 'VariableDeclarator' and node['id']['type'] == 'Identifier':
                original_name = node['id']['name']
                if original_name not in variable_map:
                    obfuscated_name = generate_random_string()
                    variable_map[original_name] = obfuscated_name
                node['id']['name'] = variable_map[original_name]
            for key in node:
                obfuscate_node(node[key])
        elif isinstance(node, list):
            for item in node:
                obfuscate_node(item)
    
    # Obfuscate the parsed JavaScript AST
    obfuscate_node(parsed_code)

    # Convert obfuscated AST back to JavaScript code (this example uses jsmin for simplicity)
    obfuscated_code = jsmin.jsmin(str(parsed_code))
    return obfuscated_code

st.title("JavaScript Obfuscator")

st.write("Enter your JavaScript code below and click 'Obfuscate' to get the obfuscated code.")

js_code = st.text_area("JavaScript Code", height=300)

if st.button("Obfuscate"):
    obfuscated_js = obfuscate_code(js_code)
    st.text_area("Obfuscated JavaScript Code", obfuscated_js, height=300)
