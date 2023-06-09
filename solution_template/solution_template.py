#########################################################################################
# This a generic template for you to use when solving more complex SnekWars challenges.
# The template has completed challenge 0 for you as an example.
#########################################################################################
import snekwars_client, json, re # import libraries as needed


#########################################################################################
# update these with the challenge number being worked on, event url, and credentials.
#########################################################################################
chal_num = 0
event_url = 'https://<event_url>'
email_address = '<email_address@email.com>'
password = '<password>'


#########################################################################################
# instantiate the snekwars client and login. 
#########################################################################################
snekwars = snekwars_client.event(event_url)
snekwars.login(email_address, password)


#########################################################################################
# print the challenge using the predefined chal_num variable.
#########################################################################################
snekwars.challenge(chal_num)


#########################################################################################
# first challenge: Submit the string returned when you call .data(0) as the solution.
# get challenge data and print it. 
# (most challenges have dynamic data that changes every time you query for it!)
#########################################################################################
data = snekwars.data(chal_num)
print('data: ')
print(data) # print the data that is returned from .data()


#########################################################################################
# here's the fun part. this is where you insert your code to solve the challenge.
# in this case, we're simply returning the data we received.
#########################################################################################
solution = data
print('solution: ')
print(solution) # print the solution that will be returned


#########################################################################################
# submit the solution and print the outcome
#########################################################################################
print(snekwars.solve(solution))
  
