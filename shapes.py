#How to draw shapes

#required 
import pygame
pygame.init()

#create colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

#create a surface
gameDisplay = pygame.display.set_mode((800,600)) #initialize with a tuple

#lets add a title, aka "caption"
pygame.display.set_caption("Drawing Shapes!")

pygame.display.update()		#only updates portion specified

gameExit = False
while not gameExit:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			gameExit = True

	gameDisplay.fill(WHITE)
	pygame.draw.rect(gameDisplay, BLACK, [400,300, 10, 100])
	pygame.draw.rect(gameDisplay, RED, [100,100, 50, 50])

	gameDisplay.fill(BLUE, rect=[200,200, 20,20])

	gameDisplay.fill(BLUE, rect=[50,50, 20,20])

	pygame.draw.circle(gameDisplay, RED, (50,100), 20, 0)
	pygame.draw.lines(gameDisplay, RED, False, [(100,100), (150,200), (200,100)], 1)

	pygame.display.update()	

pygame.quit()
quit()