import pygame
import math
from datetime import datetime


# The code has been made with help from ChatGPT. 


# Definerer uret som classe, samt dens hovedatributter        
class Watch:
    def __init__(self, radius, center, color): #Constructor metode - kaldes når der laves nye eksempler af Watch class
        self.radius = radius
        self.center = center
        self.color = color
        self.hour_angle = 0  
        self.minute_angle = 0 
        self.second_angle = 0 
        self.font = pygame.font.Font(None,36)
        #self_angles = 0 da uret kører real-time pga datetime
        #radius = 200
        #pygame.font.Font gør mig i stand til at indtegne tallene i urskiven

    # Update method beregner vinkler baseret på nuværende klokslet der hentes fra current_time = datetime.now()
    def update(self):    
        current_time = datetime.now()  
        current_hour = current_time.hour
        current_minute = current_time.minute
        current_second = current_time.second

        # Her beregnes vinklerne 
        self.hour_angle = (current_hour % 12) * 30 + current_minute * 0.5  #Bevæger sig 30 grader pr. time(360/12) samt 0.5 grader pr. minut
        self.minute_angle = current_minute * 6  # Bevæger sig 6 grader pr. minut
        self.second_angle = current_second * 6  # Samme beregning som overstående, blot pr. sekund

    # Method - Tal omkring indenfor urskiven, placeret pr. 30 grader, minus 60 grader så uret starter på 12 og ikke 0
    # Denne method tegner tallene 1-12 omkring på urskiven
    def draw_numbers(self, screen):
        for i in range (12):
            angle = math.radians(i * 30-60)
            
            text_radius = self.radius * 0.75
            text_x = self.center[0] + text_radius * math.cos(angle)
            text_y = self.center [1] + text_radius * math.sin(angle)
            
            number = str(i if i != 0 else 12)
            text_surface = self.font.render (number, True, (0,0,0))
            
            text_rect = text_surface.get_rect(center=(text_x, text_y))
            screen.blit(text_surface, text_rect)
    # Overstående skaber en overflade med tallet på sig, .blit placerer overfladen på skærmen på beregnede position
    
    # Draw method - Denne method varetager at tegne alle urets elementer
    def draw(self, screen):
        # Screen fill (clear screen), renser skærmen og skaber en hvid baggrund
        screen.fill((255, 255, 255))

    
        # farvet urskivebaggrund
        pygame.draw.circle(screen, (255,245,245), self.center, self.radius)
        
        # pyntecirkel #1
        pygame.draw.circle(screen, (94,94,93), (320,200), self.radius/3, 4)
        
        # pyntecirkel #2
        pygame.draw.circle(screen, (94,94,93), (320,280), self.radius/3, 4)
        
        # pyntecirkel #3
        pygame.draw.circle(screen, (112,58,13), (300,240), self.radius/3, 4)
        
        # pyntecirkel #4
        pygame.draw.circle(screen, (112,58,13), (340,240), self.radius/3, 4)

        # Her tegnes den ydre urskive
        pygame.draw.circle(screen, self.color, self.center, self.radius, 8)
        
        
        # Tegner tidsmærkaterne (korte for minut, mediumlange for time, lange for 3, 6, 9, 12)
        self.draw_diagonal_lines(screen)
        
        # Tegner tallene ude for tidsmærkaterne
        self.draw_numbers(screen)

        # Calculate hand lengths
        hour_hand_length = self.radius * 0.5
        minute_hand_length = self.radius * 0.65
        second_hand_length = self.radius * 0.8

        # Draw hour hand
        self._draw_hand(screen, self.hour_angle, hour_hand_length, 6, (0, 0, 0))

        # Draw minute hand
        self._draw_hand(screen, self.minute_angle, minute_hand_length, 4, (247, 224, 139))  

        # Draw second hand
        self._draw_hand(screen, self.second_angle, second_hand_length, 3, (255, 0, 0)) 
        
        # Urmidte
        pygame.draw.circle(screen, (0,0,0), self.center, 10)
        
    # Draw diagonal lines indicating minute, hour, and 3rd hour/major hour markers
    # Tegner tidsmærkaterne
    def draw_diagonal_lines(self, screen):
        for i in range(60):
            angle = math.radians(i * 6)
            
            start_x = self.center[0] + self.radius * math.cos(angle)
            start_y = self.center[1] + self.radius * math.sin(angle)
            
            # Større tidsmærkater (12, 3, 6, 9)
            if i % 15 == 0:
                end_x = self.center[0] + (self.radius * 0.85) * math.cos(angle)
                end_y = self.center[1] + (self.radius * 0.85) * math.sin(angle)
            
                            
            # Timemærkater   
            elif i % 5 == 0:
                end_x = self.center[0] + (self.radius * 0.88) * math.cos(angle)
                end_y = self.center[1] + (self.radius * 0.88) * math.sin(angle)
                
                            
            # Minutmærkater
            else:
                end_x = self.center[0] + (self.radius * 0.92) * math.cos(angle)
                end_y = self.center[1] + (self.radius * 0.92) * math.sin(angle)
                
            # Tegn tidsmærkaterne
            pygame.draw.line(screen, (0, 0, 0), (start_x, start_y), (end_x, end_y), 3)

    # Helper Method - Tegner urviserne baseret på vinkel, længde og viserens bredde
    def _draw_hand(self, screen, angle, length, width, color):
        angle_rad = math.radians(angle - 90)  # Convert angle to radians and adjust for pygame orientation
        end_x = self.center[0] + length * math.cos(angle_rad)
        end_y = self.center[1] + length * math.sin(angle_rad)
        pygame.draw.line(screen, color, self.center, (end_x, end_y), width)
    
  

# Main Function - Dette er programmets main loop, der starter Pygame vinduet, kører uret og opdaterer det real-time
def main():
    
    pygame.init()
    
    screen = pygame.display.set_mode((640, 480))
    
    # Her laves urobjektet
    my_watch = Watch(200, (320, 240), (0, 0, 0))
    
    #clock objektet bruges til at kontrollere frame rate
    clock = pygame.time.Clock()  
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Opdater urets vinkler
        my_watch.update()
        
        # Tegn uret 
        my_watch.draw(screen)
        
        # Opdater display
        pygame.display.flip()
        
        # Begræns frame rate til 60 FPS
        clock.tick(60)
        
    pygame.quit()
    

# Funktion der starter programmet
if __name__ == "__main__":
    main()
