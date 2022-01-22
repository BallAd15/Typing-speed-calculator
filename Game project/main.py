import pygame
from pygame import mixer
import random
from time import perf_counter
import mysql.connector as sqltor

mycon = sqltor.connect(host = "localhost", user = "root", passwd = "password", database = "test", charset = "utf8")
if mycon.is_connected() == False:
    print("Error connecting to MySQL database")
else:
    print("Connection successful")

#Initializing pygame
WIDTH=800
HEIGHT=600
FPS=30

WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN =(0,255,0) 
RED = (255,0,0)
BLUE = (0,0,255)

pygame.init()
screen=pygame.display.set_mode((WIDTH,HEIGHT))  #Height and Width of screen

pygame.display.set_caption("Typing Speed - WPM") #Title of the window
icon=pygame.image.load("Images/keyboard.png")
pygame.display.set_icon(icon)

sentences=["victorians once used leeches ",
      "your funny bone is actually nerves. ",
      "the chief translator of the european ",
      #"the most requested funeral song in england is by monty python.",
      "all blue-eyed people may be related. ",
      "darwin's pet tortoise died recently. ",
      #"the average person will spend six months of their life waiting for red lights to turn green.",
      #"a bolt of lightning contains enough energy to toast 100,000 slices of bread.",
      #"cherophobia is the word for the irrational fear of being happy.",
      #"you can hear a blue whale's heartbeat from two miles away.",
      #"nearly 30,000 rubber ducks were lost at sea in 1992 and are still being discovered today.",
      #"the inventor of the frisbee was turned into a frisbee after he died.",
      #"subway footlongs aren't always a foot long.",
      "curie's notebooks are still radioactive. ",]
      #"swedish blood banks notify donors when blood is used.",
      #"the netherlands is so safe, it imports criminals to fill jails.",
      #"coke saved one town from the great depression."]
random.shuffle(sentences)
 #Variables~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
username=""
first_scr=True
second_scr=False
game_status=True
correct=0
t_start=0
t_stop=0
time_t=0
wpm=0

# Fetching and Updating leaderboard ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

scores={"Muskmelon":23}
def display_sql():
    cursor = mycon.cursor()
    cursor.execute("select * from scores")
    data = cursor.fetchall()
    #Assuming data is in the form  [(name1,score1),(name2,score2),....]
    for row in data:
    	scores[row[0]]=row[1]
display(sql)

def update(name,wpm):
	global scores
	scores[name]=wpm

	cursor = mycon.cursor()
	statement_enter = "INSERT INTO scores(name,speed) VALUES('{}','{}')".format(name,wpm)
	statement_update = "UPDATE scores set speed = '{}' WHERE name = '{}'".format(wpm,name)
	flag = -1
	cursor.execute("select name from scores")
	data = cursor.fetchall()
	for i in data:
	  print(i)
	for i in data:
	  if name == i[0]:
	      flag = data.index((name,))

	if flag>=0:
	  cursor.execute(statement_update)
	  mycon.commit()
	else:
	  cursor.execute(statement_enter)
	  mycon.commit()

# Background Music ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
mixer.music.load('undertale-ruins.mp3')
mixer.music.play(-1)

# Page 1 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Background
background=pygame.image.load("Images/galaxy.png")
background=pygame.transform.scale(background, (WIDTH, HEIGHT))
#Title Icon and heading
typing_img=pygame.image.load("Images/typing.png")
#Leaderboard Image
leaderboard=pygame.image.load("Images/leaderboard.png")
leaderboard=pygame.transform.scale(leaderboard, (520, 510))

#Font
font=pygame.font.SysFont('monospace',30) #(size of font)
#Input box
input_box=pygame.Rect(350,90,600,50) # Rect(X,Y, Width, Height)


def title():
	#blit means to draw (X,Y)
	screen.blit(typing_img, (100, 20))  #Top icon image
	screen.blit(leaderboard,(140,100)) 
	title_font=font.render("WPM - Enter Username to begin!",True,(235,186,52)) #(Text, True, (RGB Colour))
	screen.blit(title_font,(220,30))

	#Input Box
	pygame.draw.rect(screen,(211,211,211),input_box,5) # (Screen,Colour,variable, thickness of box)
	input_surface=font.render(username,True,(54, 163, 209))#Font colour
	screen.blit(input_surface,(input_box.x+20,input_box.y+1))
	input_box.w= max(input_surface.get_width()+100,100)
 
	x_location = 232
	y_location = 273

	lead=sorted(scores.items(), key=lambda x: x[1], reverse=True)
	for j in lead[:6]:
		text_surface = font.render(j[0], True, (150,35,6))
		screen.blit(text_surface,(x_location,y_location))
		x_location += 250
		score_surface = font.render(f"{j[1]}WPM", True, (150,35,6))
		screen.blit(score_surface,(x_location,y_location))
		x_location-=250
		y_location += 38

#Page 2~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


count=0
senten=0

#Sentence colouring
d_colors={}
for s in range(len(sentences[:3])):
	for l in range(len(sentences[s])):
		d_colors[f"{s}{l}"]=(211,211,211)

def game_update():
	global d_colors, d_colors,correct,senten,sentences
	random.shuffle(sentences)
	d_colors={}
	for s in range(len(sentences[:3])):
		for l in range(len(sentences[s])):
			d_colors[f"{s}{l}"]=(211,211,211)
	correct=0
	count=0
	senten=0

#Buttons
home_button=pygame.image.load("Images/home.png")
replay_button=pygame.image.load("Images/replay.png")
exit_button=pygame.image.load("Images/exit.png")
#Text box 
text_box=pygame.Rect(100,45,600,400) # X,Y,WIDTH,HEIGHT
#Score box
display_score=False
score_box=pygame.Rect(100,45,600,400) 
#Score Background
score_background=pygame.transform.scale(background, (600,400))


def main():
	pygame.draw.rect(screen,(211,211,211),text_box,3)
	screen.blit(home_button,(101,500)) 
	screen.blit(replay_button,(368,500)) 
	screen.blit(exit_button,(634,500)) 
	
	#random.shuffle(sentences)
	x_location=110
	y_location=67	
	for i in range(len(sentences[:3])):
		for j in range(len(sentences[i])):
			text_surface=font.render(sentences[i][j],True,d_colors[f"{i}{j}"])
			screen.blit(text_surface,(x_location,y_location))
			x_location+=15
			if x_location>650:
				x_location=110
				y_location+=33
		y_location+=33
		x_location=110

	if display_score==True:
		#pygame.draw.rect(screen,(211,211,211),score_box)
		screen.blit(score_background,(100,45))
		score_surface=font.render(f"Your speed is {wpm}WPM",True,(54, 163, 209)) #Cyan
		screen.blit(score_surface,(220,235))

#Game Loop
running=True
while running:
	screen.fill((98,3,252)) #Background(Purple)
	screen.blit(background,(0,0)) #Background image 

	# 1) Process input (events)
	if first_scr==True:
		title()
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				running=False
			if event.type==pygame.KEYDOWN:
				if event.key==pygame.K_BACKSPACE:
					username=username[0:-1]
				elif event.key==pygame.K_RETURN:
					print(username)
					second_scr=True
					first_scr=False
				else:
					if len(username)>10:
						username=username[:11]
					username+=event.unicode

	elif second_scr==True:
		main()
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				running=False
			elif event.type==pygame.MOUSEBUTTONDOWN:
				mx,my=pygame.mouse.get_pos()
				if my>500 and my<564:
					if mx>101 and mx<165: #Home button
						first_scr=True
						second_scr=False
					elif mx>368 and mx<432: #Replay button
						game_update()
						senten=count=correct=0
						t_start=0
						t_stop=0
						display_score=False
						game_status=True
					elif mx>634 and mx<698: #Exit
						running=False
			elif event.type==pygame.KEYDOWN:
				if t_start==0:
					t_start=perf_counter()
				ch=event.unicode
				if senten==2 and count==len(sentences[2])-2: #Game ending
					game_status=False
					if t_stop==0:
						t_stop=perf_counter()
					time_t=int(t_stop-t_start)
					wpm=int(((correct/5)/time_t)*60)
					update(username,wpm)
					print(correct,time_t,wpm)
					senten=count=correct=0
					display_score=True
				if game_status==False:
					continue
				if count==len(sentences[senten]):
					count=0
					senten+=1
				if ch==sentences[senten][count]:
					d_colors[f"{senten}{count}"]=(0,255,0)
					#text_surface = pygame.font.SysFont("monospace", 20).render(ch, True, GREEN)
					#screen.blit(text_surface, ((110+(15*count)), (66+(33*senten))))
					count+=1
					correct+=1
				else:
					d_colors[f"{senten}{count}"]=(255,0,0)
					#text_surface = pygame.font.SysFont("monospace", 20).render(ch, True, RED)
					#screen.blit(text_surface, ((110+(15*count)), (66+(33*senten))))
					count+=1
	# 2) Update
	pygame.display.update()
