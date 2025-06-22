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
st.caption('Created by Will Huang.')
st.title('Random Password Generator')
st.subheader('Randomly generate a password according to your criteria.')
col1, col2, col3 = st.columns(3, gap = 'medium')

# Create a password generator.
@st.cache_resource
def _get_generator():
    return PasswordGenerator()
generator = _get_generator()

# ===== ===== ===== ===== ===== ===== ===== =====
# Password Options
# ===== ===== ===== ===== ===== ===== ===== =====

# Create a map to translate the human-readable options to
# their equivalent in the PasswordGenerator class.
inclusion_mapping = {"Yes": True, "No": False,}

# ----- ----- ----- ----- ----- ----- ----- -----
# Set the basic symbols
# ----- ----- ----- ----- ----- ----- ----- -----

with col1:

    # Create a field for entering the password length.
    generator.length = st.number_input(
        label = '**Password Length**',
        min_value = 1,
        value = 20,
        step = 1,
        format = '%d',
        key = 'length',
        label_visibility = "visible"
    )

    # Create radio buttons for which symbols should be included.
    include_lower = st.radio(
        label = '**Include lower-case letters?**',
        key = 'include_lower_case',
        options = ["Yes", "No"],
    )
    generator.include_lower_case = inclusion_mapping[include_lower]

    include_upper = st.radio(
        label = '**Include upper-case letters?**',
        key = 'include_upper_case',
        options = ["Yes", "No"],
    )
    generator.include_upper_case = inclusion_mapping[include_upper]

    include_digits = st.radio(
        label = '**Include digits (from 0 to 9)?**',
        key = 'include_digits',
        options = ["Yes", "No"],
    )
    generator.include_digits = inclusion_mapping[include_digits]

# ----- ----- ----- ----- ----- ----- ----- -----
# Set the special characters
# ----- ----- ----- ----- ----- ----- ----- -----

with col2:

    # Create a button for whether special characters should be included.
    include_special = st.radio(
        label = '**Include special characters?**',
        key = 'include_special_characters',
        options = ["Yes", "No"],
        help = 'This option determines whether special characters other than '
               'English letters and digits should be included in the password.',
        index = 1,
    )

    # Update the generator.
    generator.include_special_characters = inclusion_mapping[include_special]

    # Create radio buttons for deciding whether to use custom characters.
    special_source = st.radio(
        label = '**If special characters are used, which ones are they allowed to be?**',
        key = 'special_character_range',
        options = ["Default", "Custom"],
        captions = [
            f'Use the following characters:\n{punctuation}',
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
        generator.special_characters = punctuation
        pass_special_character = True

    # If custom characters are used, check if they meet the requirements.
    else:

        # Check if there are repeated symbols.
        counts = [custom_characters.count(x) for x in set(custom_characters)]
        if any(count > 1 for count in counts):
            st.write(':red[There are repeated custom characters. Please make sure '
                     'they are all unique.]')

        # Check if special characters are provided when required.
        elif (generator.include_special_characters == 'must') and len(custom_characters) == 0:
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
            generator.special_characters = custom_characters

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

    inclusion_list = [
        generator.include_upper_case,
        generator.include_lower_case,
        generator.include_digits,
        generator.include_special_characters,
    ]

    # Check if at least some symbols are allowed.
    if not any(inclusion_list):
        st.write('Please change the setting to allow symbols to be included in the password.')

    elif generate:

        # Check if length is shorter than the required number of symbols.
        n_must = sum(inclusion_list)
        if generator.length < n_must:
            st.write(f'The length ({generator.length}) is shorter than the minimum number of symbols that '
                     f'must show up ({n_must}).')
        elif pass_special_character:
            st.text(generator.generate())
        elif not pass_special_character:
            st.write(':red[Please resolve the issues with special character '
                     'settings and try again.]')
