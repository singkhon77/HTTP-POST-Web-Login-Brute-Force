A simple Python tool for performing HTTP POST brute-force attacks against web login forms.
Designed for local testing, labs, and security research.

Features

Brute-force web login forms

Multi-threaded

Uses password wordlists

Stops on success (optional)

Logs all attempts

Localhost protection (remote opt-in)



describe how to run both scripts, sample commands used.




Require lib
- python

- requests
-- py -3 -m pip install requests

- flask
-- py -3 -m pip install flask





wordlist_generator.py
-options
--id  <id number>      [Require]
--out  <output path>   [Require]

-Exampe Commands
-- python wordlist_generator.py --id 1310489 --out ./lists/
-- python wordlist_generator.py --id 1310489 --out ./







bruteforce_client.py
-options
--wordlist  <path of wordlist>      [Require]
--username  <target username>       [Require]
--taget-url <target url>            [Optional]  [Defualt = http://127.0.0.1:5000/login]
--threads   <number ex.1-10>        [Optional]  [Defualt = 1]
--stop-on-success   <True, False>   [Optional]  [Defualt = True]
--log   <name of log file>          [Optional]  [Defualt = logFile.txt]
--allow-remote  <True, False>       [Optional]  [Defualt = False]

-Example Commands
-- python bruteforce_client.py --username bob –-wordlist ./lists/wordlist_1310489.txt
-- python bruteforce_client.py –-username bob --thread 3 –-stop-on-success False –-wordlist ./lists/wordlist_1310489.txt –-log attem_1310489.txt
-- python bruteforce_client.py –-username bob -–stop-on-success True --threads 3 –-wordlist ./lists/wordlist_1310489.txt –-log attempt_1310489.txt
-- python script.py --wordlist passwords.txt --username admin --target-url http://example.com/login --allow-remote True

