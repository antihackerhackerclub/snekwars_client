#########################################################################################
# This script has been written for challenge 102. 
# It is based on the generic solution template for you to use when solving more complex SnekWars challenges.
# Only update the section labeled UPDATE using the instructions from the challenge.
#########################################################################################
import snekwars_client, random, base64, time, sys # import libraries as needed


#########################################################################################
# UPDATE THIS SECTION ONLY
# update these with the required variable and your credentials.
#########################################################################################
bsidesSATX_Coordinator = ""

email_address = '<email_address@email.com>'
password = '<password>'


#########################################################################################
# DO NOT UPDATE THE SECTIONS BELOW
# instantiate the snekwars client and login. 
#########################################################################################
event_url = 'https://snekwars.antihackerhackerclub.com'
snekwars = snekwars_client.event(event_url)
snekwars.login(email_address, password)
chal_num = 102


#########################################################################################
# print the challenge using the predefined chal_num variable.
#########################################################################################
snekwars.challenge(chal_num)


#########################################################################################
# Challenge code
#########################################################################################
data = snekwars.data(chal_num)
def loading_bar(total, length=30):
    for i in range(total + 1):
        if i == 50:
            time.sleep(2)
            print("\n\nI don't want to go.\n")
            time.sleep(2)
        percent = int((i / total) * 100)
        bar = '█' * int(length * i / total) + '-' * (length - int(length * i / total))
        sys.stdout.write(f"\r|{bar}| {percent}%")
        sys.stdout.flush()
        time.sleep(0.1)
    print()

if bsidesSATX_Coordinator != 'SciaticNerd':
    print("It was so simple.. you just had to update the variable. Try again.")
    exit()

print('printing .data(): ')
print(data) # print the data that is returned from .data()
time.sleep(3)
print("wait... you actually ran the script??? oof")
time.sleep(3)
print("please wait while i copy all of your passwords")
time.sleep(3)
print("just kidding.. or am i.")
time.sleep(1)
print("okay fine... 2024 BSidesSATX Coordinator regenerating to 2025 BsidesSATX Coordinator.")
loading_bar(50)
print("Regeneration complete. Please meet your new BsidesSATX Coordinator.")





#########################################################################################
# Don't worry about the man behind the curtain
#########################################################################################

def absurdly_complex_conversion(input_word):
    def rot13(s): return s.translate(str.maketrans(
        "ABCDEFGHIJKLMabcdefghijklmNOPQRSTUVWXYZnopqrstuvwxyz",
        "NOPQRSTUVWXYZnopqrstuvwxyzABCDEFGHIJKLMabcdefghijklm"
    ))

    encoded = base64.b64encode(input_word.encode()).decode()
    scrambled = rot13(encoded[::-1])

    secrets = ["QuantumBeaver", "DataSloth", "MagicFalcon", "NerdSciatic"]
    random.shuffle(secrets)
    secrets.insert(2, scrambled)

    def dig_for_truth(index, attempt=0):
        if attempt > 10:
            return None
        candidate = secrets[index]
        reversed_rot = rot13(candidate)[::-1]
        try:
            result = base64.b64decode(reversed_rot).decode()
            if result == bsidesSATX_Coordinator:
                manual_map = {
                    'S': 'P', 'c': 'i', 'i': 'n', 'a': 'w',
                    't': 'h'
                }
                output = ''.join(manual_map.get(char, '') for char in input_word[:5])
                manual_map = {
                    'N': 'e', 'e': 'e', 'r': 'l', 'd': ''
                }
                output = output + ''.join(manual_map.get(char, '') for char in input_word[6:])
                return output
        except:
            return dig_for_truth((index + 1) % len(secrets), attempt + 1)

    return dig_for_truth(0)

result = absurdly_complex_conversion(bsidesSATX_Coordinator)
print("Solution to challenge 102:", result)
solution = result


#########################################################################################
# submit the solution and print the outcome
#########################################################################################
print(snekwars.solve(solution))
  
