import Tkinter
import random
import threading
import socket
import time
import os

class game_board_cell():
	#design of each cell in the board
	#contains a background image, two color box for players move
	def __init__( self, parent, index ):

		#this frmae will hold the objects and later it will be bind to main board.
		self.cell_frame = Tkinter.Frame( parent )
		self.cell_image = Tkinter.PhotoImage( file=str(index)+'.gif' )
		self.cell_background = Tkinter.Label( self.cell_frame, image=self.cell_image, relief=Tkinter.SUNKEN  )
		self.cell_background.image = self.cell_image
		self.player1_color = Tkinter.Label(  self.cell_frame, height=1, width=2, bg='#00ff00', relief=Tkinter.RAISED, bd=4 )
		self.player2_color = Tkinter.Label(  self.cell_frame, height=1, width=2, bg='#0000ff', relief=Tkinter.RAISED, bd=4 )
		
		self.cell_background.grid( row=0, column=0, columnspan=2 )
		self.player1_color.grid( row=0, column=0 )
		self.player2_color.grid( row=0, column=1 )

		self.player1_color.grid_remove()
		self.player2_color.grid_remove()

		self.destination=None
		self.celltype=0	#0=None, 1=ladder, 2=snake






class diceroll_area():
	#design of each cell in the board
	#contains three background image
	def __init__( self, parent ):

		#this frmae will hold the objects and later it will be bind to main board.
		self.cell_frame = Tkinter.Frame( parent )
		
		self.cell_image = Tkinter.PhotoImage( file='loading.gif' )
		self.blank_background = Tkinter.Label( self.cell_frame, image=self.cell_image  )
		self.blank_background.image = self.cell_image

		self.cell_image1 = Tkinter.PhotoImage( file='dice_1.gif' )
		self.dice1_background = Tkinter.Label( self.cell_frame, image=self.cell_image1  )
		self.dice1_background.image = self.cell_image1

		self.cell_image2 = Tkinter.PhotoImage( file='dice_2.gif' )
		self.dice2_background = Tkinter.Label( self.cell_frame, image=self.cell_image2  )
		self.dice2_background.image = self.cell_image2

		self.cell_image3 = Tkinter.PhotoImage( file='dice_3.gif' )
		self.dice3_background = Tkinter.Label( self.cell_frame, image=self.cell_image3  )
		self.dice3_background.image = self.cell_image3

		self.cell_image4 = Tkinter.PhotoImage( file='dice_4.gif' )
		self.dice4_background = Tkinter.Label( self.cell_frame, image=self.cell_image4  )
		self.dice4_background.image = self.cell_image4

		self.cell_image5 = Tkinter.PhotoImage( file='dice_5.gif' )
		self.dice5_background = Tkinter.Label( self.cell_frame, image=self.cell_image5  )
		self.dice5_background.image = self.cell_image5

		self.cell_image6 = Tkinter.PhotoImage( file='dice_6.gif' )
		self.dice6_background = Tkinter.Label( self.cell_frame, image=self.cell_image6  )
		self.dice6_background.image = self.cell_image6


		
		self.blank_background.grid( row=0, column=0, columnspan=2 )
		self.dice1_background.grid( row=0, column=0, columnspan=2 )
		self.dice2_background.grid( row=0, column=0, columnspan=2 )
		self.dice3_background.grid( row=0, column=0, columnspan=2 )
		self.dice4_background.grid( row=0, column=0, columnspan=2 )
		self.dice5_background.grid( row=0, column=0, columnspan=2 )
		self.dice6_background.grid( row=0, column=0, columnspan=2 )

		self.dice1_background.grid_remove()
		self.dice2_background.grid_remove()
		self.dice3_background.grid_remove()
		self.dice4_background.grid_remove()
		self.dice5_background.grid_remove()
		self.dice6_background.grid_remove()



		self.dice_list = ( None, self.dice1_background, self.dice2_background, self.dice3_background, self.dice4_background, self.dice5_background, self.dice6_background )
		self.prev_dice = self.dice6_background

	

	def animate(self, index, parent):
		self.prev_dice.grid_remove()
		self.num=0
		for i in xrange(40):
			#print 'loop',i
			try:
				time.sleep(0.04)
				self.cell_image = Tkinter.PhotoImage(file="loading.gif", format="gif - {}".format(self.num))
				#print self.cell_image
				self.blank_background.config(image=self.cell_image)
				self.blank_background.image=self.cell_image
				self.num += 1
			except Exception as error:
				self.num = 0


		self.prev_dice = self.dice_list[index]
		self.prev_dice.grid()
		parent.update_my_move()
		











class game_interface():

	def __init__( self ):

		self.root_window = Tkinter.Tk()
		self.root_window.title("Snake_&_Ladder Client")
		self.root_window.geometry('900x640')
		self.root_window.resizable(0,0)
		#self.root_window.config( bg='red' )
		self.root_window.protocol("WM_DELETE_WINDOW", self.close_app )
		self.root_window.bind("<Destroy>", self.close_app )

		self.root_frame = Tkinter.Frame( self.root_window, bd=10 )
		self.root_frame.grid( row=0, column=0, rowspan=12, columnspan=10  )


		#create board
		self.board_cells = []

		#add a dummy widget at position 0, to remove extra board update checking on zero.
		widget = game_board_cell( self.root_frame, 0)
		self.board_cells.append( widget )

		for i in range(10):
			for j in range(1,11):
				widget = game_board_cell( self.root_frame, (10*i)+j )
				self.board_cells.append( widget )
		

		#arrange cells properly.
		grid_cell_list = self.board_cells[1:]
		row_count = 0
		for _ in range(5):
			sublist = grid_cell_list[-20:]
			grid_cell_list = grid_cell_list[:-20]

			list1 = sublist[-10:][::-1]
			column_count=0
			for cell in list1:
				cell.cell_frame.grid( row=row_count, column=column_count )
				column_count += 1
			row_count += 1


			list1 = sublist[:-10]
			column_count=0
			for cell in list1:
				cell.cell_frame.grid( row=row_count, column=column_count )
				column_count += 1

			row_count += 1



		#ladder mapping
		for pair in ( (8,26), (21,82), (43,77), (50,91), (54,93), (62,96), (66,87), (80,100) ):
			cell = self.board_cells[ pair[0] ]
			cell.destination = pair[1]
			cell.celltype = 1 #symbol of a ladder

		#snake mapping
		for pair in ( (48,9), (46,5), (44,22), (59,17), (55,7), (52,11), (69,33), (64,36), (73,1), (83,19), (92,51), (95,24), (98,28) ):
			cell = self.board_cells[ pair[0] ]
			cell.destination = pair[1]
			cell.celltype = 2


		self.info_label = Tkinter.Text( self.root_window, background='black' )#, state=Tkinter.Tkinter.DISABLED )
		self.info_label.grid( row=0, column=10, columnspan=5 )
		self.info_label.tag_configure("player", foreground='#00ff00')
		self.info_label.tag_configure("opponent", foreground='#ff0000')
		self.info_label.tag_configure("neutral", foreground='yellow')


		self.dice_area = diceroll_area( self.root_window )
		self.dice_area.cell_frame.grid( row=5, column=9,columnspan=4 )


		self.diceroll_button = Tkinter.Button( text='CLICK HERE TO ROLL DICE' )
		self.diceroll_button.bind("<Button-1>", self.play_my_move )
		self.diceroll_button.grid( row=6, column=9, columnspan=4 )


		self.init_label = Tkinter.Label( text='', width=115, height=44 )
		self.init_label.grid( row=0, column=0, rowspan=12, columnspan=12, sticky=Tkinter.W )

		self.retry_button = Tkinter.Button( text='Retry' )
		self.retry_button.grid( row=2, column=0, rowspan=12, columnspan=12, sticky=Tkinter.N )
		self.retry_button.grid_remove()
		self.retry_button.bind( "<Button-1>", lambda event : self.restart_game() )

		self.my_turn = None
		self.game_status=1

		self.current_cell = 0
		self.opponent_cell = 0



	def init_app_interface( self ):
		#enter the tkinter mainloop
		self.root_window.mainloop()



	def run( self ):
		#start the connection_manager in one thread and the interface in main thread.
		threading.Thread( target=self.connect_to_server ).start()
		self.init_app_interface()




	def restart_game( self ):
		self.retry_button.grid_remove()
		self.init_label.config( bg='#ffffff')
		self.info_label.grid()

		self.info_label.delete( 1.0, Tkinter.END )
		
		try:
			self.board_cells[ self.current_cell ].player1_color.grid_remove()
		except:
			pass

		try:
			self.board_cells[ self.opponent_cell].player2_color.grid_remove()
		except:
			pass


		self.my_turn = None
		self.game_status=1
		self.current_cell = 0
		self.opponent_cell = 0

		self.server.close()
		#print 'disconnected from server.'
		threading.Thread( target=self.connect_to_server ).start()







 
	def close_app( self ):
		try:
			self.server.send('x')
		except:
			pass
		#os.system( 'kill -9 ' + str(os.getpid()) )
		os._exit(0)




	def play_my_move( self, parent ):
		#send the dice data to server on mouse click
		if self.my_turn:
			
			#step1 : roll your dice. obtain a random number.
			self.diceroll_button.grid_remove()
			self.move = random.choice( (1,2,3,4,5,6) )
			anim_thread = threading.Thread(target=self.dice_area.animate, args=(self.move, self) )
			anim_thread.start()
		else:
			#self.info_label.config(state=Tkinter.NORMAL)

			#self.info_label.config( text='Its not your turn. Wait until opponents move...', background='#ff0000' )
			self.info_label.insert( Tkinter.END, 'Its not your turn.\nWait until opponents move...\n', 'opponent' )
			
			self.info_label.see(Tkinter.END)
			#self.info_label.config(state=Tkinter.DISABLED)





	def update_my_move( self ):

		#self.info_label.config(state=Tkinter.NORMAL)

		self.info_label.insert( Tkinter.END, 'you played : '+str(self.move)+'\n', 'player' )
		#self.info_label.see(Tkinter.END)
		#print 'you played :', move

		#step2 : remove your marker from the current position. It need to be updated.
		self.board_cells[ self.current_cell ].player1_color.grid_remove()

		msg = 'new cell : '+ str(self.current_cell)+' >>> '
		self.current_cell += self.move
		msg += str(self.current_cell)+'\n'
			
		#self.info_label.config(state=Tkinter.NORMAL)
		self.info_label.insert( Tkinter.END, msg, 'player' )
		#self.info_label.see(Tkinter.END)


		#print 'your new position :', self.current_cell
		try:
			#step3 : put your marker on the new position on the board
			self.board_cells[ self.current_cell ].player1_color.grid()

			#step4 : the current position may be a snake or ladder. so again place marker at new position
			if self.board_cells[ self.current_cell].destination != None:
				#snake or ladder found.
				if self.board_cells[ self.current_cell].celltype == 1:
					#print 'ladder found.'
					self.info_label.insert( Tkinter.END, 'Congo, You found a ladder.\n', 'neutral' )
					#self.info_label.see(Tkinter.END)
				else:
					self.info_label.insert( Tkinter.END, 'Bad luck, you got a snake bite.\n', 'neutral' )
					#self.info_label.see(Tkinter.END)
					#print 'snake bite.'

				msg = 'new cell : '+ str(self.current_cell)+' >>> '
				self.board_cells[ self.current_cell ].player1_color.grid_remove()
				self.current_cell = self.board_cells[ self.current_cell].destination
				self.board_cells[ self.current_cell ].player1_color.grid()
				msg += str(self.current_cell)+'\n'
				self.info_label.insert( Tkinter.END, msg, 'player' )
				#self.info_label.see(Tkinter.END)
				#print 'your new position:', self.current_cell

					
			#chances that the current cell is 100. which will not give any error.
			if self.current_cell == 100:
				self.board_cells[ 100 ].player1_color.grid()
				#print 'you reached the 100 cell. you won.'
				self.close_game( color='green', msg='WINNER.\nYou reached 100.')
		except:
			#some error occured means, error in setting marker.
			#current_cell is definitely more than 100. Winner condition satisfied.
			self.board_cells[ 100 ].player1_color.grid()
			#print '100 cell crossed. you won.'
			self.close_game( color='green', msg='WINNER.\nYou reached 100.')
			
		if self.move == 6:
			#print 'play again. you got a 6'
			pass
		else:
			self.root_window.config( bg='red' )
			#self.info_label.config( text=msg+'  Wait until opponents move...', background='#ff0000' )
			self.info_label.insert( Tkinter.END, 'Wait until opponents move...\n', 'opponent' )
			#self.info_label.see(Tkinter.END)
			#self.dice_area.cell_frame.grid_remove()
			self.my_turn = False

		#self.info_label.config(state=Tkinter.DISABLED)

		try:
			self.server.send( str(self.move) )
		except Exception as error:
			#print error
			pass


		self.info_label.see(Tkinter.END)
		#self.info_label.config(state=Tkinter.DISABLED)






	def update_my_board_with_opponents_move( self, move=None ):
		
		#self.info_label.config(state=Tkinter.NORMAL)
		
		if move != '0':
			#msg = '-' means opponent got a 6. So you shud skip your turn.
			if move != '-':
				try:
					#step1 : remove the opponent current marker
					self.board_cells[ self.opponent_cell ].player2_color.grid_remove()
					#print 'opponent play :', msg
					self.root_window.config( bg='red' )
					self.info_label.insert( Tkinter.END, 'opponent played : '+move+'\n', 'opponent' )
					#self.info_label.see(Tkinter.END)
						
					msg = 'new cell : '+ str(self.opponent_cell)+' >>> '
					self.opponent_cell += int(move)
					msg += str(self.opponent_cell)+'\n'
					self.info_label.insert( Tkinter.END, msg, 'opponent' )
					#self.info_label.see(Tkinter.END)


					#print 'opponent current cell :', self.opponent_cell
					try:
						self.board_cells[ self.opponent_cell ].player2_color.grid()				
						if self.board_cells[ self.opponent_cell].destination != None:
							if self.board_cells[ self.opponent_cell].celltype == 1:
								#print 'ladder found.'
								self.info_label.insert( Tkinter.END, 'your bad luck.\nopponent found a ladder.\n', 'neutral' )
								#self.info_label.see(Tkinter.END)
							else:
								#print 'snake bite.'
								self.info_label.insert( Tkinter.END, 'your good luck.\nopponent got a snake bite.\n', 'neutral' )
								#self.info_label.see(Tkinter.END)

							msg = 'new cell : '+ str(self.opponent_cell)+' >>> '
							self.board_cells[ self.opponent_cell ].player2_color.grid_remove()
							self.opponent_cell = self.board_cells[ self.opponent_cell].destination
							self.board_cells[ self.opponent_cell ].player2_color.grid()
							msg += str(self.opponent_cell)+'\n'
							self.info_label.insert( Tkinter.END, msg, 'opponent' )
							#self.info_label.see(Tkinter.END)
							#print 'opponent new position :', self.opponent_cell

						#chances that the opponent cell is 100. which will not give any error.
						if self.opponent_cell == 100:
							self.close_game( color='red', msg='LOOSER.\nOpponent reached 100')
							self.server.send('0')
					except Exception as error:
						#some error occured means, error in setting marker.
						#current_cell is definitely more than 100 for opponent. looser condition satisfied.
						self.close_game( color='red', msg='LOOSER.\nOpponent reached 100')
						self.server.send('0')
				

					if move == '6':
						self.root_window.config( bg='red' )
						self.info_label.insert( Tkinter.END, 'Opponent got one more chance.\nWaiting for opponent move...\n', 'opponent' )
						#self.info_label.see(Tkinter.END)
						#self.info_label.config( text='opponent got a 6. wait again....', background='#ff0000' )
						self.server.send('-')
					else:
						self.my_turn = True
						self.root_window.config( bg='green' )
						self.info_label.insert( Tkinter.END, 'Its your turn. Play your move.\n', 'player' )
						#self.info_label.see(Tkinter.END)
						self.diceroll_button.grid()
						#self.dice_area.cell_frame.grid()
						#self.info_label.config( text='Its your turn. PLay your move...', background='#00ff00' )
				
				except:
					self.info_label.delete( 1.0, Tkinter.END )
					self.close_game( color='yellow', msg='ERROR: Connection refused from server.')
					self.server.send('0')


			else:
				self.root_window.config( bg='green' )
				self.info_label.insert( Tkinter.END, 'Play again. You got one more chance.\n', 'player' )
				#self.info_label.see(Tkinter.END)
				self.diceroll_button.grid()
				#self.dice_area.cell_frame.grid()
				#self.info_label.config( text='play again. you got a 6.', background='#00ff00' )
				pass
		else:
			pass
		


		self.info_label.see(Tkinter.END)
		#self.info_label.config(state=Tkinter.DISABLED)









	def close_game( self, color=None, msg=None ):
		#send stop signal to the player through this function
		self.init_label.grid()
		self.init_label.config( text=msg, background=color )
		##self.info_label.config( text='Thnx for playing.', background='#ffffff')
		self.retry_button.grid()
		self.game_status=0





	def connect_to_server( self ):

		self.server = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
		self.port = 9999

		for attempt in xrange(1,3): # number of attempt to connect the server. 3-1 = 2 attepmt
			try:
				self.init_label.config( text='Attempt '+str(attempt)+': connecting to server...')
				time.sleep(1)
				self.server.connect( (socket.gethostname(),self.port) )
				#self.server.connect( ('192.168.0.109',self.port) )
				break
			except Exception as error:
				print error
				#connection failed.  reconnect attempt in 5 seconds.
				self.init_label.config( text='Connection error: Server not found.\nReconnecting in 5 sec...')
				time.sleep(5)
		else:
			###print 'limit exceed'
			self.init_label.config( text='MAX Attempt limit reached.\nAPP will be closed.' )
			time.sleep(1)
			os.system( 'kill -9 ' + str(os.getpid()) )


		#self.info_label.config(state=Tkinter.NORMAL)

		#connection established
		if self.server.recv(1) == '0':
			#player1 connection establish confirmation.
			self.init_label.config( text='Connected to the server.\nOne more player is  required to start.\nwait for one more player.\n\nSearching player2...' )
			
			if self.server.recv(1) == '0':
				#indicate that two players are connected. so begin the game.
				self.init_label.grid_remove()
				self.root_window.config( bg='green' )
				self.info_label.insert( Tkinter.END, '        YOU ARE PLAYER1\nplay your move...\n', 'player' )
				self.diceroll_button.grid()
				#self.info_label.config( text='You are player1.  Play your move...', background='#00ff00')
				self.my_turn = True
		else:
			#player2 initialization. 
			self.init_label.grid_remove()
			self.root_window.config( bg='red' )
			self.info_label.insert( Tkinter.END, '          YOU ARE PLAYER2\nWaiting for the opponent move...\n', 'opponent' )
			self.diceroll_button.grid_remove()
			#self.dice_area.cell_frame.grid_remove()
			#self.info_label.config( text='You are player2. Wait until player1 move...', background='#ff0000')
			self.my_turn = False

			#wait for the first move from opponent player only. then both client will be same.
			msg = self.server.recv(1)
			self.update_my_board_with_opponents_move( msg )



		self.info_label.see(Tkinter.END)
		#self.info_label.config(state=Tkinter.DISABLED)




		#whenever game winning condition is satisfied, game_status will be 1 and the while loop will  exit.
		while self.game_status != 0 :
			try:
				#recieves incomming data from server. and update the board.
				msg = self.server.recv(1)
				self.update_my_board_with_opponents_move( msg )
			except:
				#connection related problem found. time to stop the game.
				break

		




#main game will be started through the run() in the object of game_interface class.
app = game_interface()
app.run()


