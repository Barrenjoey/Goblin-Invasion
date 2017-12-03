'''
This is one of my first Python projects. I have used Pygame to create a simple game where you have to fight
off an invasion of goblins. The aim of the game is to progressively get harder, while leveling up and skilling
up your warrior, and eventually to see how far you can make it. As it is one of my first projects, it has
turned into a bit of a mess as i just added functionality and features on the go.
'''
#Make a level system? or make goblins spawn exponentially
# Variable attack damage or range
#
import sys
import pygame				#Importing pygame modules
import time					#Importing time module
import random

pygame.init()				#Starting pygame modules

screen_width = 1000			#Screen dimensions
screen_height = 800
white = 255,255,255			#Defining colors
brown = 128,64,0
red = 207,48,48	
green = 0,255,0	
black = 0,0,0
exp_yellow = 236,234,147

window = pygame.display.set_mode((screen_width, screen_height))	#Display window
pygame.display.set_caption('Goblin Invasion')					#Naming the window
clock = pygame.time.Clock()								#Creating a clock

#warriorImg = pygame.image.load('Warrior3.png')			#Loads Image
warrior_width = 84									#Dimensions of img
warrior_height = 82
goblinImg = pygame.image.load('Goblin1.png')			#Goblin img
levelImg = pygame.image.load("Level11.png")			#Map Img
healthDropImg = pygame.image.load('Health_droplet1.png')	#Health droplet image
health_statImg = pygame.image.load('health_stat.png')
level1_width = 2011									#Level1 img pixel dimensions
level1_height = 1944
warrior_level = 1
global used_points
used_points = 0
global warrior_maxHealth
warrior_maxHealth = 100
global healthDrops
healthDrops = []

class Rectangle(pygame.sprite.Sprite):
	def __init__(self,color,width,height):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((width, height))
		self.image.fill(color)
		self.rect = self.image.get_rect()
		
	def set_position(self, x , y):
		self.rect.x = x
		self.rect.y = y
		
def quit_game():
	pygame.quit()		
	quit()

def healthDrop(level1x,level1y,game_time):
	start = game_time
	window.blit(healthDropImg,(level1x,level1y))
	DropCoOrds = (level1x,level1y,start)
	global healthDrops
	healthDrops.append(DropCoOrds)
	return healthDrops
	
def goblin(startx,starty):
	window.blit(goblinImg,(startx,starty))	
	
def text_objects(text, font):
	textSurface = font.render(str(text), True, black)
	return textSurface, textSurface.get_rect()

def text_objects_red(text, font):
	textSurface = font.render(str(text), True, red, white)
	return textSurface, textSurface.get_rect()
	
def button(msg,x,y,w,h,ic,ac,butt=False, *args, **kwargs):       #Button creation
	mouse = pygame.mouse.get_pos()            #Mouse position
	#print(mouse)       
	click = pygame.mouse.get_pressed()        #Mouse click
	#print(click)
	if x+w > mouse[0] > x and y+h > mouse[1] > y:
		pygame.draw.rect(window, ac, (x,y,w,h))		#Button creation
		if click[0] == 1 and butt != False:
			butt(*args,**kwargs)
	else:
		pygame.draw.rect(window, ic, (x,y,w,h))
		
	smallText = pygame.font.Font('freesansbold.ttf', 40)
	textSurf, textRect = text_objects(msg, smallText)
	textRect.center = ((x+(w/2)), (y+(h/2)))
	window.blit(textSurf, textRect)	

def game_intro():
	intro = True
	while intro:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
		window.fill(white)
		largeText = pygame.font.Font('freesansbold.ttf', 115)
		TextSurf, TextRect = text_objects('Goblin Invasion', largeText)
		TextRect.center = (500,300)
		window.blit(TextSurf, TextRect)
		button('Play!',300,490,100,50,brown,red,game_loop)
		button('Quit!',600,490,100,50,red,brown,quit_game)

		pygame.display.update()
		clock.tick(15)
		
def stats_text(count,x,y):
	font = pygame.font.SysFont(None, 50)
	text = font.render(count, True, black)
	window.blit(text, (x,y))		
	
def stat_health():
	global warrior_maxHealth
	warrior_maxHealth = warrior_maxHealth + 10	
	global stats
	stats = False
	global used_points
	used_points += 1
	return warrior_maxHealth

def stat_damage():
	global attack_dmg
	attack_dmg = attack_dmg + 1	
	global stats
	stats = False
	global used_points
	used_points += 1
	return attack_dmg	
	
def stat_attkSpeed():
	global attack_speed
	attack_speed = attack_speed - 0.1
	global stats
	stats = False
	global used_points
	used_points += 1
	return attack_speed
	
def stat_attkCrit():
	global attack_crit
	attack_crit = attack_crit + 1
	global stats
	stats = False
	global used_points
	used_points += 1
	return attack_crit		
	
def stats_selection(stat_points, warrior_maxHealth, attack_dmg, attack_speed, attack_crit):
	global stats
	stats = True
	while stats:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:	
				if event.key == pygame.K_q:
					stats = False	
		pygame.draw.rect(window, brown, (200,200,600,400))
		pygame.draw.line(window, black, (500,330), (500,580), 2)
		pygame.draw.line(window, black, (270,330), (750,330), 2)		
		largeText = pygame.font.Font('freesansbold.ttf', 60)
		TextSurf, TextRect = text_objects('Stats', largeText)
		TextRect.center = (500,230)
		window.blit(TextSurf, TextRect)
		stats_text('Available Points:  ' + str(stat_points), 210, 280)
		
		window.blit(health_statImg, (200,320))							#Health
		stats_text('Health:   ' + str(warrior_maxHealth), 270, 340)		
		stats_text('+10', 520, 340)
		#window.blit(health_statImg, (200,320))							#Damage
		stats_text('Damage:    ' + str(attack_dmg), 270, 390)
		stats_text('+10', 520, 390)
		#window.blit(health_statImg, (200,320))							#Attack Speed
		stats_text('Atk Spd:    ' + str(attack_speed), 270, 440)
		stats_text('+10', 520, 440)
		#window.blit(health_statImg, (200,320))							#Crit Chance
		stats_text('Crit %:     ' + str(attack_crit), 270, 490)
		stats_text('+10', 520, 490)
		if stat_points >= 1:
			button('+',750,340,20,30,brown,red,stat_health)					#Health
			button('+',750,390,20,30,brown,red,stat_damage)					#Damage
			button('+',750,440,20,30,brown,red,stat_attkSpeed)					#Attack Speed
			button('+',750,490,20,30,brown,red,stat_attkCrit)					#Crit Chance
		#print (warrior_maxHealth)	
		pygame.display.update()
		clock.tick(15)		
	
def message_display(text):
	healthText = pygame.font.Font('freesansbold.ttf', 115)
	TextSurf, TextRect = text_objects(text, healthText)
	TextRect.center = (500,400)
	window.blit(TextSurf, TextRect)
	
def damage_text(dmg_caused, gobStartx, gobStarty):
	damageText = pygame.font.Font('freesansbold.ttf', 30)
	TextSurf, TextRect = text_objects_red(dmg_caused, damageText)
	TextRect.center = (gobStartx + 60,gobStarty + 30)
	window.blit(TextSurf, TextRect)	

def level_upTxt(text):
	lvlText = pygame.font.Font('freesansbold.ttf', 50)
	TextSurf, TextRect = text_objects(text, lvlText)
	TextRect.center = (155,770)
	window.blit(TextSurf, TextRect)	
	
def game_over():
	message_display('GAME OVER!')		
	
def health_bar(health):											#Health bar - pass in warrior_health
	pygame.draw.rect(window, black, (80,670,300,60), 5)	
	health = health/warrior_maxHealth*100
	if health <= 100 and health >90:
		pygame.draw.rect(window, red, (82,672,296,56))
	elif health <= 90 and health > 80:
		pygame.draw.rect(window, red, (82,672,266,56))
		#message_display('90')
	elif health <= 80 and health > 70:
		pygame.draw.rect(window, red, (82,672,237,56))	
	elif health <= 70 and health > 60:
		pygame.draw.rect(window, red, (82,672,207,56))	
	elif health <= 60 and health > 50:
		pygame.draw.rect(window, red, (82,672,177,56))	
	elif health <= 50 and health > 40:
		pygame.draw.rect(window, red, (82,672,148,56))
	elif health <= 40 and health > 30:
		pygame.draw.rect(window, red, (82,672,118,56))
	elif health <= 30 and health > 20:
		pygame.draw.rect(window, red, (82,672,89,56))	
	elif health <= 20 and health > 10:
		pygame.draw.rect(window, red, (82,672,59,56))
	elif health <= 10 and health > 0:
		pygame.draw.rect(window, red, (82,672,29,56))
	elif health == 0:
		game_over()
		pygame.display.update()
		time.sleep(4)
		game_intro()
		
def gob_health_bar(x):											#Health bar - pass in warrior_health
	pygame.draw.rect(window, black, (650,670,300,60), 5)	
	health = x
	if health <= 10 and health >9:
		pygame.draw.rect(window, red, (652,672,296,56))
	elif health <= 9 and health > 8:
		pygame.draw.rect(window, red, (652,672,266,56))
		#message_display('90')
	elif health <= 8 and health > 7:
		pygame.draw.rect(window, red, (652,672,237,56))	
	elif health <= 7 and health > 6:
		pygame.draw.rect(window, red, (652,672,207,56))	
	elif health <= 6 and health > 5:
		pygame.draw.rect(window, red, (652,672,177,56))	
	elif health <= 5 and health > 4:
		pygame.draw.rect(window, red, (652,672,148,56))
	elif health <= 4 and health > 3:
		pygame.draw.rect(window, red, (652,672,118,56))
	elif health <= 3 and health > 2:
		pygame.draw.rect(window, red, (652,672,89,56))	
	elif health <= 2 and health > 1:
		pygame.draw.rect(window, red, (652,672,59,56))
	elif health <= 1 and health > 0:
		pygame.draw.rect(window, red, (652,672,29,56))
	elif health == 0:		
		pass
		
def mana_bar(x):
	mana = x
	pygame.draw.rect(window, black, (80,730,300,30), 3)
	
def experience_bar(x,z):
	exp = x
	exp_level = 10
	level_2 = 10
	level_3 = 30
	level_4 = 70
	level_5 = 150
	level_6 = 310
	warrior_level = z
	pygame.draw.rect(window, black, (180,760,600,20), 3)
	if warrior_level == 1:
		exp_level = level_2
	elif warrior_level == 2:
		exp_level = level_3
	elif warrior_level == 3:
		exp_level = level_4	
	elif warrior_level == 4:
		exp_level = level_5	
	if exp == 0:
		pass
	elif exp >= exp_level*0.1 and exp < exp_level*0.2:				#596
		pygame.draw.rect(window, exp_yellow, (182,762,59,16))	#1/10 exp
	elif exp >= exp_level*0.2 and exp < exp_level*0.3:				
		pygame.draw.rect(window, exp_yellow, (182,762,119,16))	#2/10 exp
	elif exp >= exp_level*0.3 and exp < exp_level*0.4:				
		pygame.draw.rect(window, exp_yellow, (182,762,178,16))	#3/10 exp	
	elif exp >= exp_level*0.4 and exp < exp_level*0.5:				
		pygame.draw.rect(window, exp_yellow, (182,762,238,16))	#4/10 exp	
	elif exp >= exp_level*0.5 and exp < exp_level*0.6:				
		pygame.draw.rect(window, exp_yellow, (182,762,298,16))	#5/10 exp	
	elif exp >= exp_level*0.6 and exp < exp_level*0.7:				
		pygame.draw.rect(window, exp_yellow, (182,762,357,16))	#6/10 exp	
	elif exp >= exp_level*0.7 and exp < exp_level*0.8:				
		pygame.draw.rect(window, exp_yellow, (182,762,417,16))	#7/10 exp
	elif exp >= exp_level*0.8 and exp < exp_level*0.9:				
		pygame.draw.rect(window, exp_yellow, (182,762,477,16))	#8/10 exp	
	elif exp >= exp_level*0.9 and exp < exp_level:				
		pygame.draw.rect(window, exp_yellow, (182,762,536,16))	#9/10 exp	
		
def level_up(exp):
	warrior_level = 1
	level_2 = 10
	level_3 = 30
	level_4 = 70
	level_5 = 150
	level_6 = 310
	pygame.draw.rect(window, black, (130,743,50,50), 3)
	pygame.draw.rect(window, exp_yellow, (132,745,46,46))
	if exp >= level_2 and exp < level_3:
		warrior_level = 2
	elif exp >= level_3 and exp < level_4:
		warrior_level = 3	
	elif exp >= level_4 and exp < level_5:
		warrior_level = 4
	elif exp >= level_5 and exp < level_6:
		warrior_level = 5	
	level_upTxt(warrior_level)	
	return (warrior_level, level_2)
	
def dmgTxt_display(dmg_txt, game_time, dmgTxt_Start, dmg_caused, gobStartx, gobStarty):	
	if dmg_txt == True:
		damage_text(dmg_caused,gobStartx,gobStarty)
		if game_time - dmgTxt_Start >= 1:
			dmg_txt = False
			dmgTxt_Start = game_time
	else:
		dmg_txt = False	
		dmgTxt_Start = game_time
	return (dmg_txt, dmgTxt_Start)
	
def game_loop():
	mainLoop = True
	xCord = 0								#Starting Coordinate of x/y
	yCord = 0
	imgx = (screen_width * 0.45)			#Location of img on screen
	imgy = (screen_height * 0.45)
	level1x = 0
	level1y = 0
	gobStartx = random.randrange(0,screen_width)	#Starting location of goblin
	gobStarty = random.randrange(0, screen_height)
	gobx = 0
	goby = 0
	gobSpeed = 1							#Speed of goblin
	gob_maxHealth = 10
	gob_count = 1
	gob_health = gob_maxHealth
	gob_attackSpeed = 2
	gob_dmg = 5
	warriorSpeed = 4						#Speed of warrior
	global attack_dmg
	attack_dmg = 1							#Damage of Warrior
	global attack_crit
	attack_crit = 10						#Critical strike chance
	global attack_speed
	attack_speed = 1.5
	experience = 0
	dmg_caused = 0
	warrior_health = 100
	old_points = 0
	warriorImg = pygame.image.load('Warrior3.png')			#Loads Image
	img_left = pygame.transform.rotate(warriorImg, 270)
	img_right = pygame.transform.rotate(warriorImg, 90)		#Rotating image to face dircetion
	img_up = pygame.transform.rotate(warriorImg, 180)
	img_down = pygame.transform.rotate(warriorImg, 360)
	start_ticks = -5
	gob_StartTic = 0
	dmgTxt_Start = 0
	dmg_txt = False
	healthTimer = 0
	
	while mainLoop:			                   #Main game loop
		spawn_location1 = (level1x+1900,level1y+850)
		spawn_location2 = (level1x+500,level1y+0)
		spawn_locs = [spawn_location1,spawn_location2]
		game_time = pygame.time.get_ticks() /1000			#Actual game time in seconds
		#print (game_time)
		dmg = dmgTxt_display(dmg_txt, game_time, dmgTxt_Start, dmg_caused, gobStartx, gobStarty)
		dmg_txt = dmg[0]
		dmgTxt_Start = dmg[1]

		for event in pygame.event.get():	#Quit command
			if event.type == pygame.QUIT:			
				pygame.quit()
				quit()	
				
			if event.type == pygame.KEYDOWN:		#Key down events
				if event.key == pygame.K_LEFT:      #Left key down
					xCord = warriorSpeed
					warriorImg = img_left
					if gobStartx >= imgx:
						gobx = warriorSpeed     
					if gobStartx <= imgx:
						gobx = warriorSpeed	
				elif event.key == pygame.K_RIGHT:	#Right key down
					xCord = -warriorSpeed
					warriorImg = img_right
					if gobStartx <= imgx:	
						gobx = -warriorSpeed
					if gobStartx >= imgx:
						gobx = -warriorSpeed
				elif event.key == pygame.K_UP:		#Up key down
					yCord = warriorSpeed
					warriorImg = img_up
					if gobStarty >= imgy:
						goby = warriorSpeed
					if gobStarty <=	imgy:
						goby = warriorSpeed
				elif event.key == pygame.K_DOWN:	#Down key down
					yCord = -warriorSpeed
					warriorImg = img_down
					if gobStarty <= imgy:
						goby = -warriorSpeed
					if gobStarty >=	imgy:
						goby = -warriorSpeed
					
				if event.key == pygame.K_SPACE:					#Warrior main attack
					if game_time >= start_ticks + attack_speed and gobStartx > 350 and gobStartx < 550 and gobStarty > 260 and gobStarty < 460:
						critChance = random.randrange(0, 100)		#Crit Chance
						if critChance <= attack_crit and gob_health > 0:	#Crit
							gob_health += -attack_dmg*2
							#print ("Crit!")
							#print (gob_health)
							start_ticks = game_time
							dmg_caused = attack_dmg*2
							dmg_txt = True
						elif gob_health > 0:						#Normal attack
							gob_health += -attack_dmg	
							#print(gob_health)
							start_ticks = game_time
							dmg_caused = attack_dmg
							dmg_txt = True

				if event.key == pygame.K_q:
					stats_selection(stat_points, warrior_maxHealth, attack_dmg, attack_speed, attack_crit)
				
			if event.type == pygame.KEYUP:			#Releasing key
				if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
					xCord = 0
					gobx = 0
				elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
					yCord = 0
					goby = 0
						
		# print (level1y)
		# print (level1x)
		warrior_level = level_up(experience)
		stat_points = warrior_level[0] - used_points - 1

		level1x += xCord				 	#Scrolling the map
		level1y += yCord					
		gobStartx += gobx
		gobStarty += goby
		window.fill(black)
		
		wall1 = Rectangle(white, 280, 50)			#Rectangles for collision (sprite)
		wall1.set_position(level1x+510,level1y+165)	#Top
		wall2 = Rectangle(brown, 50, 280)			
		wall2.set_position(level1x+490,level1y+190)	#Left
		wall3 = Rectangle(red, 100, 50)	
		wall3.set_position(level1x+510,level1y+430)	#Bottom
		wall4 = Rectangle(brown, 50, 340)			
		wall4.set_position(level1x+490,level1y+590)	#Left
		wall6 = Rectangle(white, 100, 50)			
		wall6.set_position(level1x+510,level1y+575)	#Top
		wall7 = Rectangle(green, 50, 100)			
		wall7.set_position(level1x+750,level1y+180)	#Right
		wall8 = Rectangle(red, 170, 50)			
		wall8.set_position(level1x+620,level1y+250)	#Bottom
		wall9 = Rectangle(green, 50, 190)			
		wall9.set_position(level1x+575,level1y+270)	#Right
		wall10 = Rectangle(white, 160, 50)			
		wall10.set_position(level1x+915,level1y+165)#Top
		wall11 = Rectangle(brown, 50, 100)			
		wall11.set_position(level1x+900,level1y+180)#Left
		wall12 = Rectangle(red, 170, 50)	
		wall12.set_position(level1x+915,level1y+250)#Bottom
		wall13 = Rectangle(brown, 50, 420)			
		wall13.set_position(level1x+1070,level1y+270)#Left
		wall14 = Rectangle(green, 50, 240)			
		wall14.set_position(level1x+575,level1y+590)#Right
		wall15= Rectangle(white, 80, 50)			
		wall15.set_position(level1x+575,level1y+830)#Top
		wall16 = Rectangle(green, 50, 90)			
		wall16.set_position(level1x+610,level1y+840)#Right
		wall17 = Rectangle(red, 125, 50)	
		wall17.set_position(level1x+520,level1y+900)#Bottom
		wall18 = Rectangle(white, 320, 50)			
		wall18.set_position(level1x+755,level1y+830)#Top
		wall19 = Rectangle(green, 50, 140)			
		wall19.set_position(level1x+1155,level1y+795)#Right
		wall20 = Rectangle(brown, 50, 90)			
		wall20.set_position(level1x+745,level1y+840)#Left
		wall21 = Rectangle(red, 425, 50)	
		wall21.set_position(level1x+755,level1y+900)#Bottom
		wall22 = Rectangle(brown, 50, 80)			
		wall22.set_position(level1x+1065,level1y+795)#Left
		wall23 = Rectangle(white, 100, 50)			
		wall23.set_position(level1x+1085,level1y+785)#Top
		wall24 = Rectangle(red, 100, 50)	
		wall24.set_position(level1x+1085,level1y+650)#Bottom
		wall25 = Rectangle(green, 50, 250)			
		wall25.set_position(level1x+1155,level1y+440)#Right
		wall26 = Rectangle(green, 50, 80)			
		wall26.set_position(level1x+1220,level1y+360)#Right
		wall27 = Rectangle(green, 50, 180)			
		wall27.set_position(level1x+1300,level1y+180)#Right		
		wall28 = Rectangle(green, 50, 70)			
		wall28.set_position(level1x+1155,level1y+110)#Right	
		wall29 = Rectangle(red, 80, 50)	
		wall29.set_position(level1x+1170,level1y+400)#Bottom
		wall30 = Rectangle(red, 80, 50)	
		wall30.set_position(level1x+1250,level1y+320)#Bottom
		wall31 = Rectangle(white, 90, 50)			
		wall31.set_position(level1x+1095,level1y+95)#Top
		wall32 = Rectangle(white, 130, 50)			
		wall32.set_position(level1x+1190,level1y+160)#Top
		wall33 = Rectangle(brown, 50, 80)			
		wall33.set_position(level1x+1075,level1y+110)#Left
		
		player_block = Rectangle(white, 50, 50)		#Player block sprite for collision
		player_block.set_position((imgx+15), (imgy+10))
		
		goblin_block = Rectangle(white, 40, 40)
		goblin_block.set_position((gobStartx+25), (gobStarty+15))
		
		walls_top = pygame.sprite.Group()			#Rectangle sprite groups
		walls_left = pygame.sprite.Group()
		walls_right = pygame.sprite.Group()
		walls_bottom = pygame.sprite.Group()
		player_sprite = pygame.sprite.Group()
		enemy_sprite = pygame.sprite.Group()
		health_sprite = pygame.sprite.Group()
		
		walls_top.add(wall1,wall6,wall10,wall15,wall18,wall23,wall31,wall32)		#Adding rectangle sprites to group
		walls_left.add(wall2,wall4,wall11,wall13,wall20,wall22,wall33)
		walls_right.add(wall7,wall9,wall14,wall16,wall19,wall25,wall26,wall27,wall28)
		walls_bottom.add(wall3,wall8,wall12,wall17,wall21,wall24,wall29,wall30)
		player_sprite.add(player_block)
		enemy_sprite.add(goblin_block)
		
		walls_top.draw(window)					#Drawing to screen
		walls_left.draw(window)
		walls_right.draw(window)
		walls_bottom.draw(window)
		player_sprite.draw(window)
		enemy_sprite.draw(window)
		
		##### Bliting majority of things to screen ####
		window.blit(levelImg, (level1x,level1y))			#Display level map	
		if len(healthDrops) >= 1:					#Display health droplets with release timer
			for drop in healthDrops:
				if game_time > drop[2] + 2:
					dropLocationx = level1x+480-drop[0]
					dropLocationy = level1y+390-drop[1]
					window.blit(healthDropImg,(dropLocationx,dropLocationy))
					health_block = Rectangle(white, 20, 20)
					health_block.set_position(dropLocationx,dropLocationy)
					health_sprite.add(health_block)
					# print("drop: " + str(dropLocationx))
					# print("x: " + str(level1x))
		window.blit(warriorImg, (imgx,imgy))		#Display Img
		health_bar(warrior_health)
		gob_health_bar(gob_health)
		experience_bar(experience, warrior_level[0])
		level_up(experience)

		if level1x <= -1470:					
			level1x = -1470					#Map border
		if level1x >= 350:
			level1x = 350
		if level1y >= 360:
			level1y = 360
		if level1y <= -1430:
			level1y = -1430	

		collide_top = pygame.sprite.spritecollideany(player_block, walls_top)	#Collision groups
		collide_left = pygame.sprite.spritecollideany(player_block, walls_left)
		collide_right = pygame.sprite.spritecollideany(player_block, walls_right)
		collide_bottom = pygame.sprite.spritecollideany(player_block, walls_bottom)
		enemy_top = pygame.sprite.spritecollideany(goblin_block, walls_top)	#Goblin collision
		enemy_left = pygame.sprite.spritecollideany(goblin_block, walls_left)
		enemy_right = pygame.sprite.spritecollideany(goblin_block, walls_right)
		enemy_bottom = pygame.sprite.spritecollideany(goblin_block, walls_bottom)
		enemy_collide = pygame.sprite.spritecollideany(player_block, enemy_sprite)
		health_collide = pygame.sprite.spritecollide(player_block, health_sprite, True)
		
		if len(health_collide) != 0 and game_time > healthTimer + 1:	#Health droplet collision + timer + deletion
			for index1 in healthDrops:
				if (index1[0] - level1x) < 70 and (index1[0] - level1x) > -70 and (index1[1] - level1y) < 70 and (index1[1] - level1y) > -70:
					healthDrops.remove(index1)
					healthTimer = game_time
					if warrior_health <= warrior_maxHealth:				#Adding health with collection
						if warrior_maxHealth - warrior_health < 10:
							healthDiff = warrior_maxHealth - warrior_health
							warrior_health += healthDiff
						else:
							warrior_health += 10
		if collide_left != None:					#Collision detection
			level1x += 5 
			gobStartx += 5
		if collide_top != None:
			level1y += 5
			gobStarty += 5
		if collide_right != None:
			level1x += -5
			gobStartx += -5
		if collide_bottom != None:
			level1y += -5
			gobStarty += -5	
		
		if enemy_left != None:					#Goblin collision detection
			gobStartx += -1
		if enemy_top != None:
			gobStarty += -1
		if enemy_right != None:
			gobStartx += 1
		if enemy_bottom != None:
			gobStarty += 1	
		
		if enemy_collide != None:				
			if gobStartx > imgx:					#goblin collide
				gobStartx += 1
			elif gobStartx < imgx:
				gobStartx += -1
			elif gobStarty > imgy:
				gobStarty += 1	
			elif gobStarty < imgy:
				gobStarty += -1		
		
		if gob_health > 0:
			goblin(gobStartx,gobStarty)	#Creating goblin img from function
			if gobStartx > imgx:		
				gobStartx += -gobSpeed		#Goblin movement towards warrior
			elif gobStartx < imgx:
				gobStartx += gobSpeed
			if gobStarty > imgy:
				gobStarty += -gobSpeed
			elif gobStarty < imgy:
				gobStarty += gobSpeed
		else: 
			healthDrop(level1x,level1y,game_time)
			chosen_loc = random.choice(spawn_locs)
			gobStartx = chosen_loc[0]	#Respawn location of goblin
			gobStarty = chosen_loc[1]
			gob_health = gob_maxHealth
			goblin(gobStartx,gobStarty)
			experience += 7
			gob_count += 1
			#print (experience)	
		#if gob_health <= 0:
			#print ('Goblin Dead!')
			
		if game_time >= gob_StartTic + gob_attackSpeed and gobStartx > 380 and gobStartx < 520 and gobStarty > 290 and gobStarty < 430:	
			if warrior_health > 0:
				warrior_health += -gob_dmg				#Goblin attack 
				#print (warrior_health)
				gob_StartTic = game_time
		dmgTxt_display(dmg_txt, game_time, dmgTxt_Start, dmg_caused, gobStartx, gobStarty)
		pygame.display.update()			#Updating the loop
		clock.tick(60)					#FPS
	
#game_intro()	
game_loop()						#Runs the game loop
pygame.quit()					#Quit
quit()		