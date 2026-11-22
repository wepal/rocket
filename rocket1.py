import pygame
import math

screenWidth = 600
screenHeight = 400
rocketWidth = 20
rocketHeight = 40
x = screenWidth // 2
y = screenHeight // 2
angle = - math.pi / 2
angularVelocity = 0
velocityX = 0
velocityY = 0
gravity = 200
thrust = 1000
angularThrust = 10
running = True

pygame.init()
screen = pygame.display.set_mode((screenWidth, screenHeight))
clock = pygame.time.Clock()

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

	screen.fill("black")

	# Draw the rocket as a rotated triangle.
	rocketPoints = [
		(rocketHeight / 2, 0),
		(-rocketHeight / 2, -rocketWidth / 2),
		(-rocketHeight / 2, rocketWidth / 2)
	]
	rotatedPoints = [
		(
			int(x + pointX * math.cos(angle) - pointY * math.sin(angle)),
			int(y + pointX * math.sin(angle) + pointY * math.cos(angle))
		)
		for pointX, pointY in rocketPoints
	]
	pygame.draw.polygon(screen, "white", rotatedPoints)
	
	pygame.display.flip()

pygame.quit()
