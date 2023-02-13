# SimpleSSL for TicTacToe | Phase 1

## VM setup guide:
1- Download and install VirtualBox through the following link https://www.virtualbox.org/wiki/Downloads
2- Download Ubuntu ISO file through https://ubuntu.com/download/desktop
3- make sure that the virtualization is enabled on the computer you are going to use.
4- After installing the VM, do the following:
	a) click on new and name the VM as "Ubuntu" or any name you choose.
	b) choose the version to be Ubuntu (64-bit) and click on next.
	c) select the amount of memory, I selected 2048 MB of RAM.
	d) select "Create a virtual hard disk now" and click on create.
	e) select "VDI" and click on next.
	f) select "Dynamically allocated" and click on next.
	g) select the size of the virtual hard disk, I selected 20 GB.
	h) now click on the settings, go to System, change Processors to 2.
	i) go to Display, choose maximum Video Memory
	j) Start the VM, and select the start-up disk (Ubuntu ISO file that we downloaded earlier)
	   and complete the installation process.
5- Now that you have installed the Ubunto, make sure to download python and pip tool on it.


## How to play the game:
1- copy the .py files (server.py, client.py, tttgame.py) to the virtual machine.
2- run the server.py file on your local machine,
   you will see the IPv4 address of that machine in the terminal after running the program.
3- now use the Ubuntu terminal to run the client.py file after making sure that the server is running on your local machine.
4- now enter the server IPv4 address that you have acquired in step 2
5- the server side always plays 'X', and the client side always plays 'O'.
6- the connection will be closed after there is a winner or a tie result.
7- you can test the previous steps between 2 local machines instead of a VM and a local machine.


## Source code URLs:
1- tic-tac-toe game: https://dev.to/jamesshah/the-classic-tictactoe-game-in-python-cpi
2- TCP socket program (server.py, client.py): https://www.techwithtim.net/tutorials/socket-programming

## Important Notes:
- you can notice that most of the tic-tac-toe source code and the TCP socket program have been modified to match the project requirements.




# SimpleSSL for TicTacToe | Phase 2

## What is needed to run the game in this phase:
1- Follow the VM setup guid in Phase 1 notes (in case you want to test it on a VM).
2- After having the (server.py, client.py, tttgame.py) files copied to the VM or other local machine, make sure you have python and pip installed on that machine.
3- You need to install PyCryptodome module using pip.
4- run server.py on your local machine and client.py on the VM, or run the server and the client on 2 different local machines.

## URLs:
1- Online tool used to verify the encryption/decryption: https://gchq.github.io/CyberChef/
	* to run the tool:
		- add "AES Encrypt" to the Recipe section.
		- Specify all the parameters.
		- Add the plaintext to the Input section and observe the output.

## Important Notes:
- the KEY is hardcoded and the IV will be regenerated every new match.
- if you are using a VM, then only use it as a client. However, local machines can be used as servers or clients.



# SimpleSSL for TicTacToe | Phase 3
-----------------------------------
## What is needed to run the game in this phase:
1- Follow the VM setup guid in Phase 1 notes.
2- After having the (server.py, server2.py, client.py, client2.py, tttgame.py) files copied to the VM an other local machine, make sure you have python and pip installed on the machines.
3- PyCryptodome module should be installed from Phase 2.
4- run server.py/server2.py on your local machine and client.py/client2.py on the VM.
5- After every test, it is preferred to clear the terminal on both sides.

## important Notes:
- hashlib module has been imported to the server and client python files and was used to hash data wherever needed in the project.
- Make sure you modify the code and add the appropriate	values.
- To simplify running the test cases, server2.py represents Trudy posing as Bob and client2.py represents Trudy posing as Alice.
- For test case 1: run server.py on your local machine and client.py on the VM.	(Normal Test Case)
- For test case 2: run server2.py on your local machine and client.py on the VM.(Trudy posing as Bob)
- For test case 3: run server.py on your local machine and client2.py on the VM.(Trudy posing as Alice)

