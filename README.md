# Introduction

This is a simple web-based application that randomly generates passwords. You can specify criteria 
such as password length and which symbols should appear. 

If you have multiple online accounts that require passwords to log in, or if you need to refresh your password 
periodically, this app will suggest to you a new password quickly and easily while complying with password 
requirements. The randomness will also make your password stronger and harder to guess.     

# How to Use This App

In a typical password, there are 4 groups of symbols:

- Upper-case English letters
- Lower-case English letters
- Digits (from 0 to 9)
- Special characters (i.e., characters not in the other groups above)

In the app's interface, you can specify whether the generated password will contain symbols from these groups:

- **Must include**: The password will include at least one symbol from this group.
- **Never include**: The password will never include any symbol from this group.
- **Randomly decide**: The password will randomly include any number of symbols from this group, possibly none at all.

In case the required password contains / should not contain certain special characters in the default setting, 
you can also provide your own custom set of special symbols.

Once the password criteria are set, click the "Generate" button and copy the generated password.

**App Info**

Version 2.0.0

Created by Will Huang

**License**

This code was developed by using the [Streamlit software licensed under Apache 2.0](
https://streamlit.io/deployment-terms-of-use#:~:text=The%20Streamlit%20software%20%28the%20Python%20library%29%20is%20open-sourced,and%20deployment%20service%29%20is%20proprietary%20to%20Snowflake%20Inc.).