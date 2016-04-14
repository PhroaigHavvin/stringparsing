# stringparsing
A simple string parsing script for use in chats

INSTALL INSTRUCTIONS:

The chat.py module requires the lxml package to work properly. To ensure this is installed properly run either:

installLinux.sh - works for most distributions of Linux

installCygwin.sh - works for most versions of Cygwin




USING chat.py:

The chat.py can be executed directly with python or used in a larger application or script. When running chat.py by itself, you will be
prompted to enter a string. Once this is done, your JSON string will be printed to the console for you to view.

If you are using the chat.py module inside your own application or script, you will be calling the getMatchesJSON(string) function, where
string is the text you want to find matches on.




UNIT TESTS:

This module also uses doctest for unit testing. While the unit tests are not completely comprehensive, this allows for very basic sanity
checking to ensure the module is working correctly. To see the output of the unit tests, pass the -v argument which will add verbose
output of the unit tests status.
