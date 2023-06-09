# Installation
To install the snekwars_client run the following commands:
```
$ git clone https://github.com/antihackerhackerclub/snekwars_client
$ cd snekwars_client
$ pip install .
```

# Use
To use the client you must have two pieces of information provided by AHHC.  You must have the Address of the SnekWars server and a registration code.  With those two pieces of information you can create your account as follows:

```
$ import snekwars_client
>>> snekwars = snekwars_client.event("https://address_provided_by_AHHC")
>>> snekwars.register_account("Email Address", "Your Display Name","Your Chosen Password", "Registration code provide by AHHC")
>>> snekwars.login("Email Address","Your Chosen Password")
```

Once your account the account is created and logged in you can use the following methods to interact with the server:
 - ```snekwars.challenge(<challenge number>)``` - Retrieve and show the challenge.
 - ```snekwars.data(<challenge number>)``` - Retrieve and show a sample of the data. If True is second argument data is unzipped for you.
 - ```snekwars.solve(<your solution>)``` - Submit the solution for the last data you queried.
 - ```snekwars.scoreboard()``` - Retrieve and show the scoreboard.
 - ```snekwars.change_displayname('<new_displayname>')``` - Set your displayname on the scoreboard.
 - ```snekwars.logout()``` - Log out from your current session.
 - ```snekwars.change_password('<current_password>', '<new_password>')``` - Change the password for the logged on account from current to new.
 - ```print(snekwars.challenge_names)``` - show a list of all loaded challenge names.


 Note: You must know the current password to change it.  The AHHC Support team can reset your password. 

