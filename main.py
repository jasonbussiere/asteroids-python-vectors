
import pygame

from core.constants import VIEW_HEIGHT, VIEW_WIDTH
from game_objects.asteroid import Asteroid

from game_objects.laser import Laser
from game_objects.ship import Ship
from systems import colisions

#intialize pygame engine
pygame.init()
view = pygame.display.set_mode((1024, 576))
pygame.display.set_caption("Asteroids")
ui_font=pygame.font.SysFont('Arial', 64, bold=True)
score_font=pygame.font.SysFont('Arial', 32, bold=True)
clock=pygame.time.Clock()

#instantiate game objects
ship=Ship(view.get_width()/2, view.get_height()/2)
asteroids=[
    Asteroid(100, 100),
    Asteroid(VIEW_WIDTH-100, 100),
    Asteroid(100, VIEW_HEIGHT-100),
    Asteroid(VIEW_WIDTH-100, VIEW_HEIGHT-100)
]
lasers:list[Laser]= []



#game loop
colision_detector=colisions.ColisionDetection()
score=0
game_over=False
running = True
while running:
    #handle quit event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False

    #get state of all keyboard keys
    keys=pygame.key.get_pressed()

    ships=[ship] if ship.is_alive() else []
    if ship.is_alive():
        #pass keys list to ship, ship handles key press behavior
        new_laser = ship.handle_input(keys)
        if new_laser:
            lasers.append(new_laser)
    else:
        game_over=True

    # update game objects position
    # create a dynamic list of all objects currently in the game
    all_objects=ships+asteroids+lasers
    for obj in all_objects:
        obj.update()

    #collision resolution
    colision_detector.resolve_group_colisions(asteroids, lasers)
    colision_detector.resolve_group_colisions(asteroids, ships)

    #clean up
    alive_asteroids=[]
    new_asteroids=[]
    for ast in asteroids:
        if ast.is_alive():
            alive_asteroids.append(ast)
        else:
            if getattr(ast, 'scored', False):
                if ast.scored:
                    score += ast.point_value

            new_asteroids.extend(getattr(ast, 'fragments', []))

    asteroids=alive_asteroids+new_asteroids
    lasers=[laser for laser in lasers if laser.is_alive()]
    
    #Render
    all_objects=ships+asteroids+lasers
    view.fill((0,0,0))
    for obj in all_objects:
        obj.draw(view)

    score_text=score_font.render(f"SCORE: {score}", True, (255, 255, 255))
    view.blit(score_text, (20, 20))

    if game_over:
        text_surface=ui_font.render("G A M E  O V E R", True, (255,0,0))
        text_x=(view.get_width() - text_surface.get_width()) /2
        text_y=(view.get_height() - text_surface.get_height()) /2
        view.blit(text_surface, (text_x, text_y))

    pygame.display.flip() #update the screen
    clock.tick(60) #run the loop at 60 frames

pygame.quit()