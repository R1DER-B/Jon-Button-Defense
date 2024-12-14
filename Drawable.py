import pygame as pg
class drawable:
    def __init__(self,Surface,Rect=None):
        self.surface=Surface
        if Rect==None:
            self.rect=Surface.get_rect()
        else:
            self.rect=Rect
        self.mask=pg.mask.from_surface(Surface)
    def draw(self, Surface):
        Surface.blit(self.surface,self.rect)
        # if self.mask:
        #     Surface.blit(self.mask.to_surface(setcolor=(0,0,255)),(self.rect.x,self.rect.y))
    def copy(self):
        return drawable(self.surface)
    def move(self,speed,target):
        distance=pg.Vector2(target[0]-self.rect.center[0],(target[1]-self.rect.center[1]))
        distance.scale_to_length(speed)
        self.rect.move_ip(distance.x,distance.y)
class polygon:
    def __init__(self,Color,Points):
        self.color=Color
        self.points=Points
        self.mask=0
        self.dollar=0
        highx,lowx,highy,lowy=self.points[0].x,self.points[0].x,self.points[0].y,self.points[0].y
        for point in self.points:
            if point.x>highx:
                highx = point.x
            elif point.x<lowx:
                lowx = point.x
            if point.y > highy:
                highy = point.y
            elif point.y < lowy:
                lowy = point.y
        Canvas=pg.Surface((highx-lowx,highy-lowy))
        self.draw(Canvas)
        self.mask=pg.mask.from_surface(Canvas)
        self.rect=pg.Rect(lowx,lowy,highx-lowx,highy-lowy)
        self.center=pg.math.Vector2(((highx+lowx)/2,(highy+lowy)/2))
    def damage(self):
        if len(self.points) > 3:
            self.points.pop(0)
            self.dollar+=1
            return True
        else:
            return False
    def draw(self,Surface):
        pg.draw.polygon(Surface,self.color,self.points)
        # if self.mask:
        #     Surface.blit(self.mask.to_surface(setcolor=(0,0,255)),(self.center.x,self.center.y))
    def move(self,speed,target):
        #change=pg.Vector2(target[0],target[1])
        distance=pg.Vector2(target[0]-self.center[0],(target[1]-self.center[1]))
        distance.scale_to_length(speed)
        for point in self.points:
            point.x+=distance.x
            point.y+=distance.y
        self.center.x+=distance.x
        self.center.y+=distance.y