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

    # Moves the camera back 2 units
    scene.camera.position -= vector3(0,-1,-1)

    # Create a cube and place it in a scene, at position (0,0,0)
    # This cube has 1 unit of side, and is red
    cube1 = Object3d("UnknownCube")
    cube1.scale = vector3(3, 3, 3)
    cube1.position = vector3(-2, 1.5, 12)
    cube1.mesh = Mesh.create_cube((1, 1, 1))
    cube1.material = Material(color(0,1,0,1), "CubeMaterial")
    scene.add_object(cube1)

    # Create a second object, and add it as a child of the first object
    # When the first object rotates, this one will also mimic the transform
    cube2 = Object3d("Cube")
    cube2.scale = vector3(8, 8, 8)
    cube2.position = vector3(-2, 4, 19)
    cube2.mesh = Mesh.create_cube((1, 1, 1))
    cube2.material = Material(color(1,1,0,1), "CubeMaterial")
    scene.add_object(cube2)

    # Create a pyramid and place it in a scene
    pyr1 = Object3d("UnknownPyramid")
    pyr1.scale = vector3(3, 3, 3)
    pyr1.position = vector3(2, 1.5, 12)
    pyr1.mesh = Mesh.create_pyramid((1, 1, 1))
    pyr1.material = Material(color(1,0,1,0), "PyramidMaterial")
    scene.add_object(pyr1)

    # Create a second object, and add it as a child of the first object
    # When the first object rotates, this one will also mimic the transform
    pyr2 = Object3d("UnknownPyramid")
    pyr2.scale = vector3(11, 11, 11)
    pyr2.position = vector3(11, 5.5, 17)
    pyr2.mesh = Mesh.create_Pyramid((1, 1, 1))
    pyr2.material = Material(color(1,1,1,0), "PyramidMaterial")
    scene.add_object(pyr2)

    # Empty List for Objects
    empty_list = []

    empty_list.append(cube1)
    empty_list.append(cube2)
    empty_list.append(pyr1)
    empty_list.append(pyr2)

    # Specify the rotation of the object. It will rotate 15 degrees around the axis given, 
    # every second
    angle = 15
    axis = vector3(0, 0, 0)
    #axis.normalize()

    # Timer
    delta_time = 0
    prev_time = time.time()

    # Keyboard Keys
    aKey = False
    dKey = False
    eKey = False
    qKey = False
    sKey = False
    wKey = False
    
    # Keys List
    keys = [ aKey, dKey, eKey, qKey, sKey, wKey ]

    # Game loop, runs forever
    while (True):
        # Process OS events
        for event in pygame.event.get():
            # Checks if the user closed the window
            if (event.type == pygame.KEYDOWN):
                if event.key == pygame.K_ESCAPE:
                    return
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

        # Walking Keys
        if aKey:
            scene.camera.position += vector3(-0.02,0,0)
        if dKey:
            scene.camera.position += vector3(0.02,0,0)
        if sKey:
            scene.camera.position += vector3(0,0,-0.02) 
        if wKey:
            scene.camera.position += vector3(0,0,0.02)
           
        # Rotate Camera
        # Right
        if (mp[0]) > 0:
            axis = vector3(0,-1,0)   
            scene.camera.rotation = q * scene.camera.rotation

        # Left
        if (mp[0]) < 0:
            axis = vector3(0,1,0)   
            scene.camera.rotation = q * scene.camera.rotation

        # Up
        if (mp[1]) > 0: 
            axis = vector3(-1, 0,0)   
            scene.camera.rotation = q * scene.camera.rotation

        # Down 
        if (mp[1]) < 0:
            axis = vector3(1, 0,0)   
            scene.camera.rotation = q * scene.camera.rotation
        
        # Up Right
        if (mp[0]) > 0 and (mp[1]) < 0:
            axis = vector3(1,-1,0)   
            scene.camera.rotation = q * scene.camera.rotation

        # Down Right 
        if (mp[0]) > 0 and (mp[1]) > 0: 
            axis = vector3(-1,-1,0)   
            scene.camera.rotation = q * scene.camera.rotation

        # Up left
        if (mp[0]) < 0 and (mp[1]) < 0: 
            axis = vector3(1,1,0)   
            scene.camera.rotation = q * scene.camera.rotation

        # Down left 
        if (mp[0]) < 0 and (mp[1]) > 0: 
            axis = vector3(-1,1,0)   
            scene.camera.rotation = q * scene.camera.rotation

        # Clears the screen with a very dark blue (0, 0, 20)
        screen.fill((0,0,0))

        # Rotates the object, considering the time passed (not linked to frame rate)
        q = from_rotation_vector((axis * math.radians(angle) * delta_time).to_np3())
        #cube1.rotation = q * cube1.rotation

        scene.render(screen)

        # Swaps the back and front buffer, effectively displaying what we rendered
        pygame.display.flip()

        # Updates the timer, so we we know how long has it been since the last frame
        delta_time = time.time() - prev_time
        prev_time = time.time()


# Run the main function
main()
