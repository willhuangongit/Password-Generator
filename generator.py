# This module contains a class for generating a password
# according to specified criteria.
# Created by Will Huang
# Version == 2.0.0

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
        include_lower_case = 'must',
        include_upper_case = 'must',
        include_digits = 'must',
        include_special_characters = 'random',
        custom_special_characters = None,
    ):

        f"""
        Create a random generator for passwords.

        Parameters
        ----------
        length: int
            The length of the password to generate.

        include_lower_case: str
            Determine whether lower-case English letters should be
            included in the password.
            - 'must': Must include at least one lower-case letter.
            - 'never': Never include any lower-case letter.
            - 'random': Randomly include any number of lower-case letter,
              possibly no lower-case letter at all.

        include_upper_case: str
            Similar to include_lower_case but for upper-case English letters.

        include_digits: str
            Similar to include_lower_case but for digits from 0 to 9.

        include_special_characters:
            Similar to include_lower_case but for ASCII punctuation symbols.

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
    def include_lower_case(self):
        """
        An indicator for how lower-case letters should appear
        in the generated password.
        - 'must': must include at least one lower-case letter.
        - 'never': do not include any lower-case letter.
        - 'random': decide randomly how many lower-case letters to include.
        """
        return self.__include_lower_case

    @property
    def include_upper_case(self):
        """
        An indicator for how upper-case letters should appear
        in the generated password.
        - 'must': must include at least one upper-case letter.
        - 'never': do not include any upper-case letter.
        - 'random': decide randomly how many upper-case letters to include.
        """
        return self.__include_upper_case

    @property
    def include_digits(self):
        """
        An indicator for how digits should appear
        in the generated password.
        - 'must': must include at least one digit.
        - 'never': do not include any digit.
        - 'random': decide randomly how many digits to include.
        """
        return self.__include_digits

    @property
    def include_special_characters(self):
        """
        An indicator for how special characters should appear
        in the generated password.
        - 'must': must include at least one special character.
        - 'never': do not include any special character.
        - 'random': decide randomly how many special characters to include.
        """
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
    def special_characters(self, x):

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
        if x not in ['must', 'never', 'random']:
            raise ValueError(
                f'include_lower_case should be "must", "never" or "random" '
                f'instead of "{x}".'
            )
        self.__include_lower_case = x

    @include_upper_case.setter
    def include_upper_case(self, x):
        if x not in ['must', 'never', 'random']:
            raise ValueError(
                f'include_upper_case should be "must", "never" or "random" '
                f'instead of "{x}".'
            )
        self.__include_upper_case = x

    @include_digits.setter
    def include_digits(self, x):
        if x not in ['must', 'never', 'random']:
            raise ValueError(
                f'include_digits should be "must", "never" '
                f'or "random instead of "{x}".'
            )
        self.__include_digits = x

    @include_special_characters.setter
    def include_special_characters(self, x):
        if x not in ['must', 'never', 'random']:
            raise ValueError(
                f'include_special_characters should be "must", "never" '
                f'or "random instead of "{x}".'
            )
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
        # Create a function for drawing random samples
        # with random length.
        # ===== ===== ===== ===== ===== ===== ===== =====

        def _get_variable_length_sample(
            population, max_n: int, mode: str
        ) -> tuple:

            """
            This function randomly decides a sample size, and then draw
            a random sample (with replacement) whose size is the randomly-
            decided sample size.

            Parameters
            ----------
            population: iterable
                The population from which to sample with replacement.

            max_n: int
                The largest sample size allowed.
                This should be at least 1. However, no sample will be
                returned if mode = 'never' (see below).

            mode: str
                This determines how many samples would be drawn randomly.
                The permitted inputs are the following:
                - 'must': The sample size is at least 1.
                - 'never': The sample size is always zero.
                - 'random': The sample size is at least 0.

            Returns
            -------
            A list containing the random elements drawn from the population.
            """

            # Check inputs.
            if not isinstance(max_n, int):
                raise TypeError(f'max_n should be an integer instead of {type(max_n)}')
            if max_n < 1:
                raise ValueError(f'max_n should not be negative; it is currently {max_n}.')

            # Determine the sample size.
            if mode == 'must':
                if max_n < 1:
                    raise ValueError(f'When mode == "must", max_n should be at '
                                     f'least 1 instead of {max_n}.')
                k = self.generator.choice(range(1, max_n + 1))
            elif mode == 'never':
                k = 0
            elif mode == 'random':
                k = self.generator.choice(range(0, max_n + 1))
            else:
                raise ValueError(
                    f'mode should be "must", "never" or "random" '
                    f'instead of "{mode}".'
                )

            # Draw random sample from all possible symbols.
            return self.generator.choices(population, k = k)

        # ===== ===== ===== ===== ===== ===== ===== =====
        # Draw samples
        # ===== ===== ===== ===== ===== ===== ===== =====

        # Identify the symbols that must be included in the
        # password as well as those that can be optional.

        must_groups = {
            key: value for key, value in self.settings.items()
            if value['Include'] == 'must'
        }

        optional_groups = {
            key: value for key, value in self.settings.items()
            if (
                (value['Include'] == 'random') and
                (len(value['Symbols']) > 0)
            )
        }

        # If special characters are included in must_groups,
        # check if there is any symbol to sample from.
        # This accounts for the possibility of customized
        # special characters.
        if (
            ('Special Characters' in must_groups.keys()) and
            (len(must_groups['Special Characters']['Symbols']) == 0)
        ):
            raise ValueError(
                f'Special symbols should be included in the password, '
                f'and yet there is no special symbol defined. '
                f'Please change the settings by either providing '
                f'special characters or not forcing them to be '
                f'in the password.'
            )


        # For the symbols that must be included, see if the
        # specified length is enough to contain them.
        if (len(must_groups) > 0) and (self.length < len(must_groups)):

            # Create a wording for which symbol groups are
            # required to be in the password.
            musts_wording = [each.lower() for each in must_groups]
            if len(musts_wording) == 1:
                musts_wording = musts_wording[0]
            else:
                musts_wording = ', '.join(musts_wording[:-1]) + \
                                ' and ' + musts_wording[-1]

            raise ValueError(
                f'There are {len(must_groups)} types of symbols ({musts_wording}) '
                f'that should be included in the password, but the length of the '
                f'password to generate is only {self.length}, which is not enough. '
                f'Please change the password requirements.'
            )

        # ===== ===== ===== ===== ===== ===== ===== =====
        # Generate a password.
        # ===== ===== ===== ===== ===== ===== ===== =====

        password = []
        n_remaining = self.length

        # Draw samples from symbol groups that must be in the password.
        while len(must_groups) > 0:

            # Get the settings for this group..
            group_name, sub_settings = must_groups.popitem()

            # Count the minimum number of symbols that should be
            # reserved for other symbol groups that must show up.
            n_reserved_groups = len(must_groups)

            # If the remaining available space is smaller than the
            # number of symbols that should be reserved, raise an error.
            if n_remaining <= n_reserved_groups:
                raise ValueError(
                    f'When generating symbols that should still be present '
                    f'in the password, the number of symbol groups that should '
                    f'still be present is {n_reserved_groups}, but the remaining length '
                    f'available is {n_remaining}, which is supposed to be larger.'
                )

            # Draw random sample.
            if (n_reserved_groups == 0) and (len(optional_groups) == 0):

                # If there's no other symbol group to draw from, then
                # the current symbol group in this loop must fill out
                # the remaining space, so draw a random sample (with
                # replacement) to fill it.
                sub_sample = self.generator.choices(
                    population = sub_settings['Symbols'],
                    k = n_remaining
                )

            else:

                # Otherwise, draw a sample with variable length,
                # but reserve enough space for the other essential
                # symbol groups.
                sub_sample = _get_variable_length_sample(
                    population = sub_settings['Symbols'],
                    max_n = n_remaining - n_reserved_groups,
                    mode = sub_settings['Include']
                )

            # Include the sub-sample in the overall password.
            password.extend(sub_sample)

            # Update n_remaining.
            n_remaining = self.length - len(password)

        # Draw samples from symbol groups that may or may not be in the password.
        while (n_remaining > 0) and (len(optional_groups) > 0):

            # Get the settings for this group.
            group_name, sub_settings = optional_groups.popitem()

            # Draw random sample.
            if len(optional_groups) == 0:

                # If there's no other symbol group to draw from, then
                # the current symbol group in this loop must fill out
                # the remaining space, so draw a random sample (with
                # replacement) to fill it.
                sub_sample = self.generator.choices(
                    population = sub_settings['Symbols'],
                    k = n_remaining
                )

            else:

                # Otherwise, draw a sample with variable length.
                sub_sample = _get_variable_length_sample(
                    population = sub_settings['Symbols'],
                    max_n = n_remaining,
                    mode = sub_settings['Include']
                )

            # Include the sub-sample in the overall password.
            password.extend(sub_sample)

            # Update n_remaining.
            n_remaining = self.length - len(password)

        # ===== ===== ===== ===== ===== ===== ===== =====
        # Convert the password to a string.
        # ===== ===== ===== ===== ===== ===== ===== =====

        # Randomly shuffle the order of the symbols in-place.
        self.generator.shuffle(password)

        # Concatenate and return the password.
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