*** Settings ***
Library    SeleniumLibrary

*** Test Cases ***
Login to localhost
    Open Browser    http://localhost:3000/login  edge
    Input Text    id=username    user
    Input Text    id=password    password
    Click Button    id=Login
    Sleep    5
    Location Should Be    http://localhost:3000/home
    Close Browser
Register to localhost
    Open Browser    http://localhost:3000/register  edge
    Input Text    id=username    user1234
    Input Text    id=password    password1234
    Input Text    id=email    user123@123.com
    Click Button    id=checkbox
    Click Button    id=register
    Sleep    3
    Location Should Be    http://localhost:3000/home
    Close Browser
Add and remove courses
    Open Browser    http://localhost:3000/login  edge
    Input Text    id=username    user
    Input Text    id=password    password
    Click Button    id=Login
    Sleep    5
    Location Should Be    http://localhost:3000/home
    ${initial_list_size}    Get Element Count    id=enrolledCourses
    Click Element    id=dropdown
    Click Element    id=Python
    Sleep    3
    ${list_size}    Get Element Count    id=enrolledCourses
    Run Keyword If    '${initial_list_size}' == '${list_size}'    Fail
    Click Element    Python_drop_button
    Sleep    3
    ${list_size}    Get Element Count    id=enrolledCourses
    Run Keyword If    '${initial_list_size}' != '${list_size}'    Fail
    Close Browser