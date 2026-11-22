import pygame
import math
import random

screenWidth = 800
screenHeight = 600
rocketHeight = 30
rocketX = screenWidth // 2
rocketY = screenHeight // 2
angle = - math.pi / 2
angularVelocity = 0
velocityX = 0
velocityY = 0
gravity = 100
thrust = 1000
angularThrust = 10
friction = 0.5
angularFriction = 3.0
targetSize = 20
targetCount = 8
targetsCatched = 0
running = True

pygame.init()
screen = pygame.display.set_mode((screenWidth, screenHeight))
clock = pygame.time.Clock()
targetFont = pygame.font.Font(None, targetSize + 2)

# load images
background = pygame.image.load("background.jpg").convert()
background = pygame.transform.scale(background, (screenWidth, screenHeight))
rocketNoFireImage = pygame.image.load("rocket.png").convert_alpha()
rocketScale = rocketHeight / rocketNoFireImage.get_height()
rocketNoFireImage = pygame.transform.scale(rocketNoFireImage, (int(rocketNoFireImage.get_width() * rocketScale), int(rocketNoFireImage.get_height() * rocketScale)))
rocketFireImage = pygame.image.load("rocket_fire.png").convert_alpha()
rocketFireImage = pygame.transform.scale(rocketFireImage, (int(rocketFireImage.get_width() * rocketScale), int(rocketFireImage.get_height() * rocketScale)))

# craete target mask for collision detection
targetSurface = pygame.Surface((targetSize, targetSize), pygame.SRCALPHA)
targetRadius = targetSize // 2
pygame.draw.circle(targetSurface, (255, 255, 255), (targetRadius, targetRadius), targetRadius)
targetMask = pygame.mask.from_surface(targetSurface)

# create random target positions and colors
targetPositions = []
targetColors = []
for _ in range(targetCount):
	targetX = random.randint(0, screenWidth - targetSize)
	targetY = random.randint(0, screenHeight - targetSize)
	targetPositions.append((targetX, targetY))
	targetColors.append((random.randint(120, 255), random.randint(120, 255), random.randint(120, 255)))

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
	velocityX *= (1 - friction * dt)
	velocityY *= (1 - friction * dt)
	angularVelocity *= (1 - angularFriction * dt)

	# apply velocity and angular velocity to position and angle
	rocketX += velocityX * dt
	rocketY += velocityY * dt
	angle += angularVelocity * dt

	# endless space
	if rocketX < 0:
		rocketX += screenWidth
	elif rocketX > screenWidth:
		rocketX -= screenWidth
	if rocketY < 0:
		rocketY += screenHeight
	elif rocketY > screenHeight:
		rocketY -= screenHeight

	# rotate the rocket image based on the current angle
	rocketImage = rocketFireImage if pygame.key.get_pressed()[pygame.K_UP] else rocketNoFireImage
	rotatedRocketImage = pygame.transform.rotate(rocketImage, -math.degrees(angle))
	rotatedRocketImageMask = pygame.mask.from_surface(rotatedRocketImage)
	
	# target collision
	for i in range(targetsCatched, targetCount):
		targetX, targetY = targetPositions[i]
		# check for collision
		x = targetX - rotatedRocketImage.get_rect(center=(rocketX, rocketY)).left
		y = targetY - rotatedRocketImage.get_rect(center=(rocketX, rocketY)).top
		colliding = rotatedRocketImageMask.overlap(targetMask, (int(x), int(y))) is not None
		if colliding:
			if i == targetsCatched:
				# Catched the correct target
				targetsCatched += 1
				if targetsCatched == targetCount:
					# You win!
					running = False
			else:
				# Game over
				running = False

	# Draw the background image.
	screen.blit(background, (0, 0))

	# Draw the remaining targets
	for i in range(targetsCatched, targetCount):
		targetX, targetY = targetPositions[i]
		targetCenter = (targetX + targetSize // 2, targetY + targetSize // 2)
		pygame.draw.circle(screen, targetColors[i], targetCenter, targetSize // 2)
		targetLabel = targetFont.render(str(i + 1), True, (0, 0, 0))
		screen.blit(targetLabel, targetLabel.get_rect(center=targetCenter))

	# Draw the rotated rocket image
	rocketRect = rotatedRocketImage.get_rect(center=(rocketX, rocketY))
	screen.blit(rotatedRocketImage, rocketRect)
	
	pygame.display.flip()

pygame.quit()
