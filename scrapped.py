#elif self.rect2[0][1]>=self.rect2[2][1] and self.incr: 
        #    self.rect2 = self.rect2 + narrowToWide
        #    if abs(self.rect2[0][0])
        '''
        if (self.rect2[0][1]<self.rect2[2][1] #LHS taller
            or self.rect2[2][0]-self.rect2[0][0]>=0): #haven't crossed yet? 
            #print('hello')
            if not self.incr:
                self.rect2 = self.rect2+wideToNarrow
            else:
                self.rect2 = self.rect2+narrowToWide
            ##if not self.dir:
            #self.rect = self.rect + np.array([[-5, 0],[5,0]])
            #if abs((self.rect[0][0]-self.rect[1][0]))>=self.xWidth:
                #self.rect2 = self.rect2+wideToNarrow
            #if (abs(self.rect2[0][0]-self.rect2[2][0])>=self.xWidth):
            ##    if  self.rect2[0][0]-self.rect2[2][0])<=0:
             #       self.rect2 = np.array([r2, r3, r0, r1])
             #       self.dir = not self.dir
             #       return
            #elif self.rect2[2][0]<self.rect2[0][0]:
            #    self.dir = not self.dir
            #    return
            #elif 
            #self.rect[0][0]-=0.1 
            #self.rect[1][1]+=0.1 
            #elif abs(self.rect[0][0]-self.rect[0][1])<0:
            #else:
                #self.rect = self.rect + np.array([[5, 0],[-5,0]]) 
            #    self.rect2 = self.rect2+narrowToWide
                #if abs(self.rect[0][0]-self.rect[1][0])<=0:
                #if (abs(self.rect2[0][0]-self.rect2[2][0])<=0):
            #    if (abs(self.rect2[0][0]-self.rect2[2][0])>=self.xWidth):
            #        self.rect2 = np.array([r2, r3, r0, r1])
            #        self.dir = not self.dir
            #        return
                #elif self.rect2[2][0]>self.rect2[0][0]:
                #    self.dir = not self.dir
                #    return 
                #self.rect[0][0]+=0.1
                #self.rect[1][1]+=0.1
        elif (self.rect2[0][1]>self.rect2[2][1] #RHS taller
                or self.rect2[2][0]-self.rect2[0][0]>=0): 
            if self.incr and self.rect2[0][0]-self.rect2[2][0]<=self.xWidth:
                self.rect2 = self.rect2+narrowToWide
            else:
                self.rect2 = self.rect2+wideToNarrow
        else:
            #print('error')
            #self.rect2 = np.array([r2, r3, r0, r1])
            self.incr = not self.incr
        self.counter+=1
        print(self.incr, self.counter)
        #print(}
        '''
        '''
        #if self.rect[0][0]-self.width/2>=2:
        if not self.dir:
            #self.rect = self.rect + np.array([[-5, 0],[5,0]])
            #if abs((self.rect[0][0]-self.rect[1][0]))>=self.xWidth:
            self.rect2 = self.rect2+wideToNarrow
            #if (abs(self.rect2[0][0]-self.rect2[2][0])>=self.xWidth):
            if (abs(self.rect2[0][0]-self.rect2[2][0])<=0):
                self.rect2 = np.array([r2, r3, r0, r1])
                self.dir = not self.dir
                return
            #elif self.rect2[2][0]<self.rect2[0][0]:
            #    self.dir = not self.dir
            #    return
            #elif 
            
            #self.rect[0][0]-=0.1 
            #self.rect[1][1]+=0.1 
        #elif abs(self.rect[0][0]-self.rect[0][1])<0:
        else:
            #self.rect = self.rect + np.array([[5, 0],[-5,0]]) 
            self.rect2 = self.rect2+narrowToWide
            #if abs(self.rect[0][0]-self.rect[1][0])<=0:
            #if (abs(self.rect2[0][0]-self.rect2[2][0])<=0):
            if (abs(self.rect2[0][0]-self.rect2[2][0])>=self.xWidth):
                self.rect2 = np.array([r2, r3, r0, r1])
                self.dir = not self.dir
                return
            #elif self.rect2[2][0]>self.rect2[0][0]:
            #    self.dir = not self.dir
            #    return 
            #self.rect[0][0]+=0.1
            #self.rect[1][1]+=0.1
        '''
