
import pygame
from random import randint
import math
from sklearn.cluster import KMeans

WIDTH = 1150
HEIGHT = 600
GRAY = (214,214,214)
RED = (255,0,0)
RED = (0,0,255)
GREEN = (0,255,0)
BLACK = (0,0,0)
WHITE = (255,255,255)
BG_PANNEL = (249,255,230)
BG = GRAY
YELLOW = (147,153,35)
PURPLE = (255,0,255)
SKY = (0,255,255)
ORANGE = (255,125,25)
GRAPE = (100,25,125)
GRASS = (55,155,65)

colors= [RED, SKY , YELLOW , ORANGE , GRAPE , GRASS , PURPLE , GREEN , GRAY ,WHITE ]

class button:
    def __init__(self,text,coordinate,width,height):
        self.text = text
        self.coordinate = coordinate
        self.width = width
        self.height = height
        font = pygame.font.SysFont('sans', 40)
        self.font_text = font.render(str(text),True,WHITE)
        
    def draw_rect(self):
        pygame.draw.rect(screen,BLACK,(self.coordinate[0],self.coordinate[1],self.width,self.height))
        screen.blit(self.font_text,(self.coordinate[0]+5,self.coordinate[1]+5))

    def check_click(self):
        mouse = pygame.mouse.get_pos()
        if (self.coordinate[0] < mouse[0]< self.coordinate[0]+self.width and self.coordinate[1] < mouse[1] < self.coordinate[1] + self.height):
            return True
        else:
            return False



pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Kmeans Visualization")
clock = pygame.time.Clock()
running = True

run_positive_btn = button("+",(850,60),50,50)
run_negative_btn = button("-",(940,60),50,50)
run_btn = button("Run",(850,160),150,50)
random_btn = button("Random",(850,260),150,50)
algorithm_btn = button("Algorithm",(850,410),150,50)
reset_btn = button("Reset",(850,480),150,50)

btns = [run_positive_btn,run_negative_btn,run_btn,random_btn,algorithm_btn,reset_btn]
points = []
error_txt = 0
K = 0
clusters = []
dot_color = BLACK
label = []
#distance between 2 points
def distance(p1,p2):
    return math.sqrt(math.pow(p1[0]-p2[0],2) + math.pow(p1[1]-p2[1],2))

while running:
    clock.tick(60)
    screen.fill(BG)
    #Draw pannel
    pygame.draw.rect(screen,BLACK,(50,50,700,500))
    pygame.draw.rect(screen,BG_PANNEL,(55,55,690,490))
    #Draw interface
    for i in range(len(btns)):
        btns[i].draw_rect()
    #End draw interface

    #Draw text 
    font = pygame.font.SysFont('sans', 40)
    error_text = font.render("Error : "+ str(error_txt),True,BLACK)
    screen.blit(error_text,(850,340))

    K_text = font.render("K = " + str(K),True,BLACK)
    screen.blit(K_text,(1030,60))

    #Draw mouse position when mouse is in the panel
    mouse = pygame.mouse.get_pos()
    if ( 55 < mouse[0] < 55+690 and 55 < mouse[1] < 55+490):
        font = pygame.font.SysFont("sans",20)
        text_mouse = font.render("("+ str(mouse[0]-55) + "," + str(mouse[1]-55) + ")",True, BLACK)
        screen.blit(text_mouse,(mouse[0],mouse[1]))
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            running = False

        if (event.type == pygame.MOUSEBUTTONDOWN):
            if(run_positive_btn.check_click()):
                if (K<9):
                    K+=1
            if(run_negative_btn.check_click()):
                if (K>0):
                    K-=1
            if(random_btn.check_click()):
                clusters = []
                label = []
                for i in range(K):
                    random_point = [randint(0,700)+55,randint(0,500)+55]
                    clusters.append(random_point)


            #Algorithm btn
            if (algorithm_btn.check_click()):
                try:
                    kmeans = KMeans(n_clusters = K).fit(points)
                    #print(kmeans.cluster_centers_)
                    label = kmeans.predict(points)
                    clusters = kmeans.cluster_centers_
                except:
                    print("Error K is invalid")
            #Reset btn
            if (reset_btn.check_click()):
                label = []
                K = 0
                error_txt = 0
                points = []
                clusters = []
                
            if (run_btn.check_click()):
                    #Assign points to closet clusters
                    label = []
                    if (len(clusters) == 0  ):
                        continue
                    for i in range(len(points)):
                        distances = [] #create a list distance when we start click run button
                        for k in range(len(clusters)):
                            distance_result = distance(points[i],clusters[k])
                            distances.append(distance_result)
                        #min value in distances list
                        min_distance = min(distances)
                        #Find index of cluster 
                        # for t in range(len(clusters)):
                        #     if(distance(points[i],clusters[t]) == min_distance):
                        #             label.append(t)
                        label_points = distances.index(min_distance)
                        label.append(label_points)
                    #Update lusters
                    new_cluster_x = 0
                    new_cluster_y = 0
                    for i in range(K):
                       
                        sum_x =0
                        sum_y =0
                        count = 0
                        for j in range(len(points)):
                            if (label[j] == i):
                                #index of label is index of point in points List
                                sum_x += points[j][0]
                                sum_y += points[j][1]
                                count +=1

                            if count !=0:
                                new_cluster_x = int(sum_x / count) 
                                new_cluster_y = int(sum_y /count)
                                clusters[i] = [new_cluster_x,new_cluster_y]
                    error_txt = 0
                    for i in range(K):
                        for j in range(len(points)):
                            if(label[j] == i):
                                error_txt += distance(clusters[i],points[j])
                    error_txt = int(error_txt)
            #create point on panel

            if ( 55 < mouse[0] < 55+690 and 55 < mouse[1] < 55+490):
                label = []
                point = mouse[0],mouse[1] ##
                points.append(point)
            
    #Draw many dots in 
    
    for i in range(len(points)):      
        pygame.draw.circle(screen,BLACK,(points[i][0],points[i][1]),6)
        if (len(label) != 0):
            pygame.draw.circle(screen,colors[label[i]],(points[i][0],points[i][1]),4)
        else:
            pygame.draw.circle(screen,WHITE,(points[i][0],points[i][1]),4)
            
    #Draw clusters
    #if start_clusters:
    for i in range(len(clusters)):
        pygame.draw.circle(screen,colors[i],clusters[i],8)
        #start_clusters = False
    pygame.display.flip()
pygame.quit()