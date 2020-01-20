# Import pygame into our program
import pygame
import pygame.freetype
import time

from scene import *
from object3d import *
from mesh import *
from material import *
from color import *

# Define a main function, just to keep things nice and tidy
def main():
    # Initialize pygame, with the default parameters
    pygame.init()
    
    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)
    mp = pygame.mouse.get_rel()

    # Define the size/resolution of our window
    res_x = 640
    res_y = 480

    # Create a window and a display surface
    screen = pygame.display.set_mode((res_x, res_y))

    # Create a scene
    scene = Scene("Scene")
    scene.camera = Camera(False, res_x, res_y)

    # Moves the camera back 3 units
    scene.camera.position += vector3(1, 1, 1)
    scene.camera.position -= vector3(0,0,3)

    # Create a pyramid and place it in a scene, at position (1,1,1)
    # This pyramid has 1 unit of side, and is red
    pyr1 = Object3d("UnknownPyramid")
    pyr1.scale = vector3(1, 1, 1)
    pyr1.position = vector3(1, 1, 1)
    pyr1.mesh = Mesh.create_pyramid((1, 1, 1), None)
    pyr1.material = Material(color(1,0,0,1), "PyramidMaterial")
    scene.add_object(pyr1)

    # Create a second object, and add it as a child of the first object
    # When the first object rotates, this one will also mimic the transform
    pyr2 = Object3d("ChildPyramid")
    pyr2.position += vector3(-0.75, -0.25, 0)
    pyr2.mesh = Mesh.create_pyramid((0.5, 0.5, 0.5))
    pyr2.material = Material(color(0,1,0,1), "PyramidMaterial")
    pyr1.add_child(pyr2)

    # List of the objects
    objects = [ pyr1, pyr2 ]

    # Specify the rotation of the object. It will rotate 15 degrees around the axis given, 
    # every second
    angle = 15
    axis = vector3(0, 0, 0)
    
    # Timer
    delta_time = 0
    prev_time = time.time()

    # Keys
    aKey = False
    dKey = False
    eKey = False
    qKey = False
    sKey = False
    wKey = False
    upKey = False
    downKey = False
    leftKey = False
    rightKey = False
    pUpKey = False
    pDownKey = False

    # Keys List
    keys = [ aKey, dKey, eKey, qKey, sKey, wKey, upKey, downKey, leftKey, rightKey, pUpKey, pDownKey ]

    run = True
    obj = True

    # Game loop, runs forever
    while (run):
        # Process OS events
        for event in pygame.event.get():
            # Checks if the user closed the window
            if (event.type == pygame.KEYDOWN):
                if (event.key == pygame.K_ESCAPE):
                    run = False

                if (event.key == pygame.K_a):
                    aKey = True

                if (event.key == pygame.K_d):
                    dKey = True

                if (event.key == pygame.K_e):
                    eKey = True

                if (event.key == pygame.K_q):
                    qKey = True

                if (event.key == pygame.K_s):
                    sKey = True

                if (event.key == pygame.K_w):
                    wKey = True

                if (event.key == pygame.K_UP):
                    upKey = True

                if (event.key == pygame.K_DOWN):
                    downKey = True

                if (event.key == pygame.K_LEFT):
                    leftKey = True

                if (event.key == pygame.K_RIGHT):
                    rightKey = True

                if (event.key == pygame.K_PAGEUP):
                    pUpKey = True

                if (event.key == pygame.K_PAGEDOWN):
                    pDownKey = True

            elif (event.type == pygame.KEYUP):

                if (event.key == pygame.K_a):
                    aKey = False

                if (event.key == pygame.K_d):
                    dKey = False

                if (event.key == pygame.K_e):
                    eKey = False

                if (event.key == pygame.K_q):
                    qKey = False

                if (event.key == pygame.K_s):
                    sKey = False

                if (event.key == pygame.K_w):
                    wKey = False

                if (event.key == pygame.K_UP):
                    upKey = False

                if (event.key == pygame.K_DOWN):
                    downKey = False

                if (event.key == pygame.K_LEFT):
                    leftKey = False

                if (event.key == pygame.K_RIGHT):
                    rightKey = False

                if (event.key == pygame.K_PAGEUP):
                    pUpKey = False

                if (event.key == pygame.K_PAGEDOWN):
                    pDownKey = False

        # Moves the object
        if aKey:
            scene.camera.position += scene.camera.left() * 0.001

            if dKey:
                scene.camera.position += scene.camera.right() * 0.001

            if sKey:
                scene.camera.position += scene.camera.back() * 0.001

            if wKey:
                scene.camera.position += scene.camera.forward() * 0.001

            if qKey:
                scene.camera.position += vector3(0,0,0.01)

            if eKey:
                scene.camera.position -= vector3(0,0,0.01)
            
        # Rotates the object, considering the time passed (not linked to frame rate)
        q = from_rotation_vector((axis * math.radians(angle) * delta_time).to_np3())
        scene.camera.rotation = scene.camera.rotation * q

        #Rotate keys
        if upKey:
            axis = vector3(3,0,0)
            scene.camera.rotation = q * scene.camera.rotation

        if downKey:
            axis = vector3(-3,0,0)
            scene.camera.rotation = q * scene.camera.rotation

        if leftKey:
            axis = vector3(0,3,0)
            scene.camera.rotation = q * scene.camera.rotation

        if rightKey:
            axis = vector3(0,-3,0)
            scene.camera.rotation = q * scene.camera.rotation

        if pUpKey:
            axis = vector3(0,0,3)
            scene.camera.rotation = q * scene.camera.rotation

        if pDownKey:
            axis = vector3(0,0,-3)
            scene.camera.rotation = q * scene.camera.rotation
            
       # Stop objects that are behind the camera from being renderered
        if (dot_product(scene.camera.forward(), pyr1.forward() - scene.camera.position) < 0):
            if (obj):
                scene.remove_object(pyr1)
                obj = False
        else:
            obj = True
            if (pyr1 not in scene.objects):
                scene.add_object(pyr1)

        scene.render(screen)

        # Clears the screen with a very dark blue (0, 0, 20)
        screen.fill((0,0,0))
        
        scene.render(screen)

        # Swaps the back and front buffer, effectively displaying what we rendered
        pygame.display.flip()

        # Updates the timer, so we we know how long has it been since the last frame
        delta_time = time.time() - prev_time
        prev_time = time.time()


# Run the main function
main()
