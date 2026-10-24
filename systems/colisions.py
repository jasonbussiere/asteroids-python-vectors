
class ColisionSystem:
    def handle_colisions(self, ship, lasers, asteroids):
        #collision engine laser vs asteroid
        all_objects=[ship]+lasers+asteroids
        

        results={"game_over":False}
        for i in range (len(all_objects)):
            for j in range (i+1, len(all_objects)):
                obj1=all_objects[i]
                obj2=all_objects[j]

                if obj1.has_collided_with(obj2):
                    obj1.on_impact_with(obj2)
                    obj2.on_impact_with(obj1)

        new_fragments=[]
        for asteroid in asteroids:
            if not asteroid.is_alive():
                new_fragments.extend(asteroid.split())

                #skip asteroids already marked for dead
                #if asteroid in dead_asteroids:
                    #continue
    
                #if laser has collided with an asteroid make them for dead
                #if laser.collides_with(asteroid):
                   # dead_lasers.add(laser)
                    #dead_asteroids.add(asteroid)
    
                    #print("BOOM! Asteroid has shattered!")
    
                    #new_asteroids.extend(asteroid.split())
    
                    #stop checking if a collision occurs
                    #break
    
        #for asteroid in asteroids:
            #if asteroid in dead_asteroids:
                #continue
    
            destroyed=ship.collides_with(asteroid)
            print(f"Destroyed: {destroyed}")
            if destroyed:
                results["Game_Over"]=True
                break
        return results

        #CLEAN UP: keep only live lasers and live asteroids
        lasers[:]=[laser for laser in lasers if laser.is_alive() ]
        asteroids[:]=[asteroid for asteroid in asteroids if asteroid.is_alive() ]
        asteroids.extend(new_fragments)