import pygame
import math

screenWidth = 600
screenHeight = 400
rocketHeight = 30
x = screenWidth // 2
y = screenHeight // 2
angle = - math.pi / 2
angularVelocity = 0
velocityX = 0
velocityY = 0
gravity = 200
thrust = 1000
angularThrust = 10
friction = 1
angularFriction = 1
running = True

pygame.init()
screen = pygame.display.set_mode((screenWidth, screenHeight))
clock = pygame.time.Clock()

# load images
background = pygame.image.load("background.jpg").convert()
background = pygame.transform.scale(background, (screenWidth, screenHeight))
rocketNoFireImage = pygame.image.load("rocket.png").convert_alpha()
rocketScale = rocketHeight / rocketNoFireImage.get_height()
rocketNoFireImage = pygame.transform.scale(rocketNoFireImage, (int(rocketNoFireImage.get_width() * rocketScale), int(rocketNoFireImage.get_height() * rocketScale)))
rocketFireImage = pygame.image.load("rocket_fire.png").convert_alpha()
rocketFireImage = pygame.transform.scale(rocketFireImage, (int(rocketFireImage.get_width() * rocketScale), int(rocketFireImage.get_height() * rocketScale)))

while running:
	dt = clock.tick(60) / 1000
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	# acceleration
	velocityY += gravity * dt
	if pygame.key.get_pressed()[pygame.K_LEFT]:
		angularVelocity -= angularThrust * dt
	if pygame.key.get_pressed()[pygame.K_RIGHT]:
		angularVelocity += angularThrust * dt
	if pygame.key.get_pressed()[pygame.K_UP]:
		velocityX += thrust * dt * math.cos(angle)
		velocityY += thrust * dt * math.sin(angle)

	# friction
	velocityX *= (1-friction * dt)
	velocityY *= (1-friction * dt)
	angularVelocity *= (1-angularFriction * dt)

	# apply velocity and angular velocity to position and angle
	x += velocityX * dt
	y += velocityY * dt
	angle += angularVelocity * dt

	# endless space
	if x < 0:
		x += screenWidth
	elif x > screenWidth:
		x -= screenWidth
	if y < 0:
		y += screenHeight
	elif y > screenHeight:
		y -= screenHeight

	# Draw the background image.
	screen.blit(background, (0, 0))

	# Draw the rotated rocket image
	rocketImage = rocketFireImage if pygame.key.get_pressed()[pygame.K_UP] else rocketNoFireImage
	rotatedRocketImage = pygame.transform.rotate(rocketImage, -math.degrees(angle))
	rocketRect = rotatedRocketImage.get_rect(center=(x, y))
	screen.blit(rotatedRocketImage, rocketRect)
	
	pygame.display.flip()

pygame.quit()
