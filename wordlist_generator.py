
import argparse
import os
import random
import string

# input from command
parser = argparse.ArgumentParser(description = 'Description of the progeam :  This program used to generate wordlist')
parser.add_argument('--id', type=int, required =True, help='ID number')
parser.add_argument('--out', type=str, required =True, help='Output path')

args = parser.parse_args()
student_id = args.id


# generate passwords
def generate_passwd(student_id, count= 300):
    random.seed(student_id)
    passwords = set()


    base_words = [
        'Password', 'Admin', 'User', 'Login', 'Welcome', 'Hello',
        'System', 'Access', 'Account', 'Secure', 'Master', 'Root','Super', 'Manager', 'Guest', 'Test', 'Demo', 'Default','Key', 'Code', 'Pass', 'Fanshawe', 'Fol', 'Private'
    ]


    years = ['2020', '2021', '2022', '2023', '2024', '2025',
             '20', '21', '22', '23', '24', '25']


    symbols = ['!', '@', '#', '$', '%', '&', '*', '!@',             '#$','@@','!!', '##', '$$', '_', '-', '.']

    # prepend
    for word in base_words:
        for symbol in symbols[:8]:
            pwd = f"{student_id}{word}{symbol}"
            passwords.add(pwd)
            if len(passwords) >= count:
                break

    # append
    for word in base_words:
        for symbol in symbols[:8]:
            pwd = f"{word}{student_id}{symbol}"
            passwords.add(pwd)
            if len(passwords) >= count:
                break

    # id+year
    for year in years:
        for symbol in symbols[:6]:
            pwd = f"{student_id}{year}{symbol}"
            passwords.add(pwd)
            pwd = f"{year}{student_id}{symbol}"
            passwords.add(pwd)
            if len(passwords) >= count:
                break


    # check for 300 words
    charset = string.ascii_letters + string.digits + "!@#$%&*_-. "
    i = 0
    while len(passwords) < count:
        tail = ''.join(rnd.choice(charset) for _ in range(4 + (i % 3)))
        candidate = f"{student_id}{tail}"
        passwords.add(candidate)
        i += 1



    passwords = sorted(list(passwords))[:count]

    # reset random seed
    random.seed()

    # print("this is real number of password : " + str(len(passwords)))

    return passwords



# write to file
file_name = "wordlist_" + str(student_id) + ".txt"

dir_path = args.out

file_path = os.path.join(dir_path, file_name)

os.makedirs(dir_path, exist_ok=True)

passwords = generate_passwd(student_id, count=300)

with open(file_path, "w") as f:
    print ("Written 300 passwords to " + file_path)
    for pwd in passwords:
        f.write(pwd + "\n")
