# This module is used to generate the web app for the password generator.
# Created by Will Huang
# Version == 1.0.0

# Dependency versions
# Python == 3.10.10
# streamlit == 1.26.0
# generator == 2.0.0

# Imports
import streamlit as st
from string import ascii_lowercase, ascii_uppercase, digits, punctuation
from generator import PasswordGenerator

# ===== ===== ===== ===== ===== ===== ===== =====
# Initiate the streamlit application.
# ===== ===== ===== ===== ===== ===== ===== =====

st.set_page_config(
    page_title = 'Random Password Generator',
    layout = "wide"
)
st.title('Random Password Generator')
st.subheader('Randomly generate a password according to your custom criteria.')
col1, col2, col3 = st.columns(3, gap = 'medium')


# Create a password generator.
@st.cache_resource
def _get_generator():
    return PasswordGenerator()

@st.cache_data
def _get_output():
    return ''

g = _get_generator()
output = _get_output()

# ===== ===== ===== ===== ===== ===== ===== =====
# Password Options
# ===== ===== ===== ===== ===== ===== ===== =====

# Create a map to translate the human-readable options to
# their equivalent in the PasswordGenerator class.
mapping = {
    "Must include": 'must',
    "Never include": 'never',
    "Decide randomly": 'random'
}

# ----- ----- ----- ----- ----- ----- ----- -----
# Set the basic symbols
# ----- ----- ----- ----- ----- ----- ----- -----

with col1:

    # Create a field for entering the password length.
    g.length = st.number_input(
        label = '**Password Length**',
        min_value = 1,
        value = 12,
        step = 1,
        format = '%d',
        key = 'length',
        label_visibility = "visible"
    )

    # Create radio buttons for which symbols should be included.
    include_lower = st.radio(
        label = '**Include lower-case letters?**',
        key = 'include_lower_case',
        options = ["Must include", "Never include", "Decide randomly"],
    )
    g.include_lower_case = mapping[include_lower]

    include_upper = st.radio(
        label = '**Include upper-case letters?**',
        key = 'include_upper_case',
        options = ["Must include", "Never include", "Decide randomly"],
    )
    g.include_upper_case = mapping[include_upper]

    include_digits = st.radio(
        label = '**Include digits (from 0 to 9)?**',
        key = 'include_digits',
        options = ["Must include", "Never include", "Decide randomly"],
    )
    g.include_digits = mapping[include_digits]

# ----- ----- ----- ----- ----- ----- ----- -----
# Set the special characters
# ----- ----- ----- ----- ----- ----- ----- -----

with col2:

    # Create a button for whether special characters should be included.
    include_special = st.radio(
        label = '**Include special characters?**',
        key = 'include_special_characters',
        options = ["Must include", "Never include", "Decide randomly"],
        help = 'This option determines whether special characters other than '
               'English letters and digits should be included in the password.',
        index = 2,
    )

    # Update the generator.
    g.include_special_characters = mapping[include_special]

    # Create radio buttons for deciding whether to use custom characters.
    special_source = st.radio(
        label = '**If special characters are used, which ones are they allowed to be?**',
        key = 'special_character_range',
        options = ["Default", "Custom"],
        captions = [
            f'Use the following ASCII characters:\n{punctuation}',
            'Use your own custom list below.'
        ],
    )

    # Create a field for entering customized special characters.
    custom_characters = st.text_input(
        label = 'Custom Special Characters',
        key = 'custom_special_characters',
        value = '',
        label_visibility = 'hidden',
        placeholder = 'Enter special characters other than English letters or digits.'
    )

    # Set the default value for whether to allow password generation
    # due to special character formatting.
    pass_special_character = False

    # If default special characters are used, set them in the generator.
    if special_source == "Default":
        g.special_characters = punctuation
        pass_special_character = True

    # If custom characters are used, check if they meet the requirements.
    else:

        # Check if there are repeated symbols.
        counts = [custom_characters.count(x) for x in set(custom_characters)]
        if any(count > 1 for count in counts):
            st.write(':red[There are repeated custom characters. Please make sure '
                     'they are all unique.]')

        # Check if special characters are provided when required.
        elif (g.include_special_characters == 'must') and len(custom_characters) == 0:
            st.write(
                ':red[Special symbols must be provided.]'
            )

        # Make sure special characters do not include English letters or digits.
        elif set(custom_characters).intersection(
            [*ascii_lowercase, *ascii_uppercase, *digits]
        ):
            st.write(':red[Special characters should not include English letters or '
                     'digits.]')

        else:
            pass_special_character = True
            g.special_characters = custom_characters

# ----- ----- ----- ----- ----- ----- ----- -----
# Generate password
# ----- ----- ----- ----- ----- ----- ----- -----

with col3:

    # Create a button for generating password.
    generate = st.button(
        label = 'Generate Password',
        key = 'generate_password',
        type = 'primary',
    )

    if generate and pass_special_character:
        st.text(g.generate())
    elif  generate and not pass_special_character:
        st.write(':red[Please resolve the issues with special character '
                 'settings and try again.]')