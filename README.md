
# SimpleSSL for TicTacToe

## VM setup guide:
- Download and install VirtualBox through the following link https://www.virtualbox.org/wiki/Downloads
- Download Ubuntu ISO file through https://ubuntu.com/download/desktop
- make sure that the virtualization is enabled on the computer you are going to use.
- After installing the VM, do the following:
	- a) click on new and name the VM as "Ubuntu" or any name you choose.
	- b) choose the version to be Ubuntu (64-bit) and click on next.
	- c) select the amount of memory, I selected 2048 MB of RAM.
	- d) select "Create a virtual hard disk now" and click on create.
	- e) select "VDI" and click on next.
	- f) select "Dynamically allocated" and click on next.
	- g) select the size of the virtual hard disk, I selected 20 GB.
	- h) now click on the settings, go to System, change Processors to 2.
	- i) go to Display, choose maximum Video Memory
	- j) Start the VM, and select the start-up disk (Ubuntu ISO file that we downloaded earlier)
	   and complete the installation process.
- Now that you have installed the Ubunto, make sure to download python and pip tool on it.

## How to play the game:
- Copy the .py files (server.py, client.py, tttgame.py) to the virtual machine.
- Run the server file on your local machine, you will see the IPv4 address of that machine in the terminal after running the program.
- Now use the Ubuntu terminal on the VM to run the client file after making sure that the server is running on your local machine.
- Now enter the server IPv4 address that you have acquired in step 2
- The server side always plays 'X', and the client side always plays 'O'.
- Enjoy a "secure" TicTacToe game.

## What is needed to run the game in this phase:
1. Follow the VM setup guide.
2. After having the (server.py, server2.py, client.py, client2.py, tttgame.py) files copied to the VM an other local machine, make sure you have python and pip installed on the machines.
3. Install PyCryptodome module using pip.
4. Run server.py/server2.py on your local machine and client.py/client2.py on the VM.
5. After every test, it is preferred to clear the terminal on both sides.

## important Notes:
- you can notice that most of the tic-tac-toe source code and the TCP socket program have been modified to match the project requirements.
- the KEY is hardcoded and the IV will be regenerated every new match.
- if you are using a VM, then only use it as a client. However, local machines can be used as servers or clients.
- hashlib module has been imported to the server and client python files and was used to hash data wherever needed in the project.
- Make sure you modify the code and add the appropriate	values.
- To simplify running the test cases, server2.py represents Trudy posing as Bob and client2.py represents Trudy posing as Alice.
- For test case 1: run server.py on your local machine and client.py on the VM.	(Normal Test Case)
- For test case 2: run server2.py on your local machine and client.py on the VM.(Trudy posing as Bob)
- For test case 3: run server.py on your local machine and client2.py on the VM.(Trudy posing as Alice)

## Source code and URLs:
- tic-tac-toe game: https://dev.to/jamesshah/the-classic-tictactoe-game-in-python-cpi
- TCP socket program (server.py, client.py): https://www.techwithtim.net/tutorials/socket-programming
- Online tool used to verify the encryption/decryption: https://gchq.github.io/CyberChef/
	* to run the tool:
		- add "AES Encrypt" to the Recipe section.
		- Specify all the parameters.
		- Add the plaintext to the Input section and observe the output.


