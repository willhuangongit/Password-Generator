# This module contains a class for generating a password
# according to specified criteria.
# Created by Will Huang
# Version == 3.0.0

# Dependency versions
# Python == 3.10.10

# Imports
import random
from string import ascii_lowercase, ascii_uppercase, digits, punctuation

# Classes
class PasswordGenerator:

    def __init__(
        self,
        length = 10,
        include_lower_case = True,
        include_upper_case = True,
        include_digits = True,
        include_special_characters = True,
        custom_special_characters = None,
    ):

        f"""
        Create a random generator for passwords.

        Parameters
        ----------
        length: int
            The length of the password to generate.

        include_lower_case: bool
            Determine whether lower-case English letters should be considered for the password.

        include_upper_case: bool
            Determine whether upper-case English letters should be considered for the password.

        include_digits: bool
            Determine whether digits from 0 to 9 should be considered for the password.

        include_special_characters: bool
            Determine whether special characters should be considered for the password.

        custom_special_characters: None or str
            If the user prefers to use special symbols that are different from
            the default ASCII punctuation symbols, then pass a string containing
            these symbols.
        """

        # Set the scope for all special characters.
        if custom_special_characters is None:
            self.special_characters = punctuation
        else:
            self.special_characters = custom_special_characters

        # Set other properties.
        self.generator = random.Random()
        self.length = length
        self.include_lower_case = include_lower_case
        self.include_upper_case = include_upper_case
        self.include_digits = include_digits
        self.include_special_characters = include_special_characters

    # ===== ===== ===== ===== ===== ===== ===== =====
    # Properties
    # ===== ===== ===== ===== ===== ===== ===== =====

    @property
    def generator(self):
        """The random.Random class instance from the standard Python
        library used to generate random passwords."""
        return self.__generator

    @property
    def special_characters(self):
        """
        These are all the special characters that may be included
        in the generated password.
        """
        return self.__special_characters

    @property
    def length(self):
        """The length of the password generated."""
        return self.__length

    @property
    def include_lower_case(self) -> bool:
        """An indicator for whether lower case English letters should appear in the generated password."""
        return self.__include_lower_case

    @property
    def include_upper_case(self) -> bool:
        """An indicator for whether upper case English letters should appear in the generated password."""
        return self.__include_upper_case

    @property
    def include_digits(self) -> bool:
        """An indicator for whether digits should appear in the generated password."""
        return self.__include_digits

    @property
    def include_special_characters(self) -> bool:
        """An indicator for whether special characters should appear in the generated password."""
        return self.__include_special_characters

    # ===== ===== ===== ===== ===== ===== ===== =====
    # Setters
    # ===== ===== ===== ===== ===== ===== ===== =====

    @generator.setter
    def generator(self, x):
        if not isinstance(x, random.Random):
            raise TypeError(f'generator should be an instance of '
                            f'{random.Random} instead of {type(x)}')
        self.__generator = x

    @special_characters.setter
    def special_characters(self, x: str):

        # Check input.
        if not isinstance(x, str):
            raise TypeError(f'special_characters should be an string '
                            f'instead of {type(x)}')
        # if len(x) == 0:
        #     raise ValueError(f'There is no special character provided.')

        # Prevent the user from duplicating the default symbols.
        x_set = set(x)
        default_symbols = set(ascii_uppercase + ascii_lowercase + digits)
        common = x_set.intersection(default_symbols)
        if len(common) > 0:
            raise ValueError(
                f'special_characters should not include the following '
                f'symbols: {common}.'
            )

        # Prevent the user from submitting duplicated special characters.
        counts = {symbol: x.count(symbol) for symbol in x_set}
        duplicates = {s: c for s, c in counts.items() if c > 1}
        if duplicates:
            raise ValueError(
                f'The string submitted to special_characters contains '
                f'duplicated symbols. Here are the duplicated symbols and '
                f'how many times they appear:\n{duplicates}.'
            )

        self.__special_characters = x

    @length.setter
    def length(self, x):
        if not isinstance(x, int):
            raise TypeError(f'length should be an integer instead of {type(x)}')
        if (x <= 0):
            raise ValueError(f'x should be positive instead of {x}.')
        self.__length = x

    @include_lower_case.setter
    def include_lower_case(self, x):
        if not isinstance(x, bool):
            raise ValueError(f'include_lower_case should be boolean instead of {x}')
        self.__include_lower_case = x

    @include_upper_case.setter
    def include_upper_case(self, x):
        if not isinstance(x, bool):
            raise ValueError(f'include_upper_case should be boolean instead of {x}')
        self.__include_upper_case = x

    @include_digits.setter
    def include_digits(self, x):
        if not isinstance(x, bool):
            raise ValueError(f'include_digits should be boolean instead of {x}')
        self.__include_digits = x

    @include_special_characters.setter
    def include_special_characters(self, x):
        if not isinstance(x, bool):
            raise ValueError(f'include_special_characters should be boolean instead of {x}')
        self.__include_special_characters = x

    @property
    def settings(self):

        """View the settings for this random password generator."""

        return {
            'Lower Case': {
                'Symbols': ascii_lowercase,
                'Include': self.include_lower_case,
            },
            'Upper Case': {
                'Symbols': ascii_uppercase,
                'Include': self.include_upper_case,
            },
            'Digits': {
                'Symbols': digits,
                'Include': self.include_digits,
            },
            'Special Characters': {
                'Symbols': self.special_characters,
                'Include': self.include_special_characters,
            },
        }

    # ===== ===== ===== ===== ===== ===== ===== =====
    # Methods
    # ===== ===== ===== ===== ===== ===== ===== =====

    def generate(self, verify = True) -> 'str':

        """
        Generate a random password.
        The password is generated according to the following properties
        of this class instance:

        - length
        - special_characters
        - include_lower_case
        - include_upper_case
        - include_digits
        - include_special_characters

        For details, please refer to the documentation for these properties.

        Parameters
        ----------
        verify: bool
            If True, then check if the generated password complies with
            the requirements (properties) specified above.

        Returns
        -------
        A string containing the generated password.
        """

        # ===== ===== ===== ===== ===== ===== ===== =====
        # Collect the set of all symbols to use.
        # ===== ===== ===== ===== ===== ===== ===== =====

        # Identify the symbols that must be included.

        groups_to_include = {
            key: value for key, value in self.settings.items()
            if value['Include']
            and len(value['Symbols']) > 0
        }

        # For the symbols that must be included, see if the
        # specified length is enough to contain them.
        # For example, if the 3 categories of upper case, lower case and digits are all required,
        # but that the maximum length of the password is 2, then raise an error.

        if (len(groups_to_include) > 0) and (self.length < len(groups_to_include)):

            # Create a wording for which symbol groups are required to be in the password.
            musts_wording = [each.lower() for each in groups_to_include]
            if len(musts_wording) == 1:
                musts_wording = musts_wording[0]
            else:
                musts_wording = ', '.join(musts_wording[:-1]) + \
                                ' and ' + musts_wording[-1]

            raise ValueError(
                f'There are {len(groups_to_include)} types of symbols ({musts_wording}) '
                f'that should be included in the password, but the length of the '
                f'password to generate is only {self.length}, which is not enough. '
                f'Please change the password requirements.'
            )

        # ===== ===== ===== ===== ===== ===== ===== =====
        # Generate a password.
        # ===== ===== ===== ===== ===== ===== ===== =====

        password = []
        n_remaining_groups = len(groups_to_include)
        remaining_length = self.length

        for group_settings in groups_to_include.values():
            
            # Draw a sample of symbols (with replacement).
            n_remaining_groups -= 1
            sample_source = group_settings['Symbols']

            if len(sample_source) == 0:
                continue
            elif n_remaining_groups == 0:
                draw_size = remaining_length
            else:
                draw_size = self.generator.randrange(
                    start = 1, 
                    stop = remaining_length - n_remaining_groups
                    )

            sub_sample = self.generator.choices(
                population = group_settings['Symbols'],
                k = draw_size,
                )
            
            # Count the actual sample size in case the list of all symbols being drawn from is empty.
            actual_sample_size = len(sub_sample)

            # Update values.
            password.extend(sub_sample)
            remaining_length -= actual_sample_size

        # ===== ===== ===== ===== ===== ===== ===== =====
        # Convert the password to a string.
        # ===== ===== ===== ===== ===== ===== ===== =====

        self.generator.shuffle(password)
        password = ''.join(password)

        # ===== ===== ===== ===== ===== ===== ===== =====
        # Verify whether the result matches the
        # requirements.
        # ===== ===== ===== ===== ===== ===== ===== =====

        if verify:

            # Check length.
            if len(password) != self.length:
                raise ValueError(
                    f'The length of the generated password\n{password}\n'
                    f'is {len(password)}, which is different from the '
                    f'required length of {self.length}.')

            # Create a function to check if the password includes or
            # excludes specific symbols.
            def _verify_inclusion(pw: str, reference, reference_name: str, mode: str):

                common = set(reference).intersection(pw)

                if (mode == 'must') and (not common):
                    raise ValueError(
                        f'The generated password\n{pw}\ndoes not '
                        f'include {reference_name} when it should. '
                        f'Please fix the code.'
                    )

                elif (mode == 'never') and common:
                    raise ValueError(
                        f'The generated password\n{pw}\nincludes '
                        f'{reference_name} when it should not. '
                        f'Please fix the code.'
                    )

            # Apply the function to do the verification.
            _verify_inclusion(
                pw = password,
                reference = ascii_lowercase,
                reference_name = 'lower-case letters',
                mode = self.include_lower_case
            )

            _verify_inclusion(
                pw = password,
                reference = ascii_uppercase,
                reference_name = 'upper-case letters',
                mode = self.include_upper_case
            )

            _verify_inclusion(
                pw = password,
                reference = digits,
                reference_name = 'digits',
                mode = self.include_digits
            )

            _verify_inclusion(
                pw = password,
                reference = self.special_characters,
                reference_name = 'special characters',
                mode = self.include_special_characters
            )

        return password