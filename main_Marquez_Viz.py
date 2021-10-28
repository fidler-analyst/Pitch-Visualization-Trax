# pitch GIF

#libraries
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from mpl_toolkits.mplot3d.axes3d import Axes3D
from PIL import Image
import glob



#define strike zone
sz = pd.DataFrame(columns = ['x','y','z'])
sz.loc[0,:] = -.71, 0, 1.5                      #bottom left
sz.loc[1,:] = -.71, 0, 3.5                      #top left
sz.loc[2,:] = .71, 0, 3.5                       #top right
sz.loc[3,:] = .71, 0, 1.5                       #bottom right
sz.loc[4,:] = -.71, 0, 1.5                      #bottom left
 

pitch_data = pd.read_csv('Marquez_last10Ks.csv')
step = np.linspace(0,1,11)
pitch_path = pd.DataFrame(columns = ['Pitcher', 'Batter', 'Pitch', 'Out', 'V', 'xpath','ypath','zpath'])

fig_count = 0
fig_countt = 0

for r in list(range(0,len(pitch_data))):  
    
    #the t loop creates the pitch_path dataframe which takes the release point and increment through the break
    for t in list(range(0,11)):
        
        pitch_path.loc[t, 'Pitcher'] = pitch_data.loc[r, 'Pitcher' ]
        pitch_path.loc[t, 'Batter'] = pitch_data.loc[r, 'Batter']
        pitch_path.loc[t, 'Pitch'] = pitch_data.loc[r, 'TaggedPitchType']
        pitch_path.loc[t, 'Out'] = pitch_data.loc[r, 'PitchCall']
        
        pitch_path.loc[t, 'V'] = round(pitch_data.loc[r, 'RelSpeed'], 1)
    
        pitch_path.loc[t, 'ypath'] = pitch_data.loc[r, 'y0'] - pitch_data.loc[r, 'YBreak']*t/10            #y path
        pitch_path.loc[t, 'xpath'] = pitch_data.loc[r, 'x0'] + pitch_data.loc[r, 'HorzBreak']*(t**2/100)   #x path
        pitch_path.loc[t, 'zpath'] = pitch_data.loc[r, 'z0'] + pitch_data.loc[r, 'VertBreak']*(t**2/100)   #z path


    #create figure
    for i in list(range(1, len(pitch_path))):
        fig = plt.figure(num = i)
        ax = plt.axes(projection = '3d')
        #ax.set_box_aspect()
     
        #plot the strike zone
        ax.plot3D(sz.x[0:2], sz.y[0:2], sz.z[0:2], 'black')
        ax.plot3D(sz.x[1:3], sz.y[1:3], sz.z[1:3], 'black')
        ax.plot3D(sz.x[2:4], sz.y[2:4], sz.z[2:4], 'black')
        ax.plot3D(sz.x[3::], sz.y[3::], sz.z[3::], 'black')
         
        ax.axes.set_xlim3d(left = -4, right = 4)                #x axis limit
        ax.axes.set_zlim3d(bottom = 0, top = 7)                 #z axis limit
       
        ax.view_init(3,-55)                                     #camera position to match point of view of Coors Field
       
        #plot ball path, up to ith position
        ax.plot3D(pitch_path.xpath[0:i], pitch_path.ypath[0:i], pitch_path.zpath[0:i], color = 'red')
       
        #plot ball position, last i
        ax.scatter3D(pitch_path.xpath[i], pitch_path.ypath[i], pitch_path.zpath[i])
       
        #adds pither, pitch type, velocity, batter and swinging/looking to figure
        ax.text(-7, 0, 27, pitch_data.loc[r, 'Pitcher'])           
        ax.text(-7, 0, 26, (pitch_data.loc[r, 'TaggedPitchType'] + ':  '+ str(round(pitch_data.loc[r, 'RelSpeed'],1))+' mph'))   
        ax.text(-7, 0, 25, (pitch_data.loc[r, 'Batter']+ ':  '+pitch_data.loc[r, 'PitchCall']))    
         
        plt.xticks(color = 'w')                     #remove x axis ticks for clarity
        plt.yticks(color = 'w')                     #remove y axis ticks for clarity
        ax.zaxis.set_ticklabels([])                 #remove z axis ticks for clarity
        for line in ax.zaxis.get_ticklines():
            line.set_visible(False)   
            
        #change the scale of the plot source4
        x_scale = 1
        y_scale = 3
        z_scale = 1
        scale=np.diag([x_scale, y_scale, z_scale, 1.0])
        scale=scale*(1.0/scale.max())
        scale[3,3]=1.0
        
        def short_proj():
            return np.dot(Axes3D.get_proj(ax), scale)
        ax.get_proj=short_proj
       
        ax.grid(False)                           #remove figure grid
        fig.set_size_inches(10,10)               #set figure size
        plt.axis('off')                          #remove axis
        
        name = 'fig' + str(fig_count).zfill(3) + '.png'    #figure name
        fig.savefig(name)                                  #save figure
        fig_count+=1                                       #next figure
     
    
 
#generate GIF #source3
frames = []
imgs = glob.glob("*.png")
imgs.remove('Coors.PNG')

#change transparency of Coors Field  #source2
Coors = Image.open('Coors.png')
Coors.putalpha(100)
Coors.save('Coors.png')
 
#overlay each pitch image and make into a GIF
for i in imgs:
    new_frame = Image.open(i)  
    new_frame.paste(Coors, (120,250), Coors)  #source1  
    frames.append(new_frame)
    
    
    
frames[0].save('Marquez.gif', format = 'GIF', append_images = frames[1:], save_all = True, duration = 225, loop = 0)


#Sources
#source1: #https://moonbooks.org/Articles/How-to-overlay--superimpose-two-images-using-python-and-pillow-/
#source2: #https://wallpapersafari.com/coors-field-wallpaper/
#source3: #https://pythonprogramming.altervista.org/png-to-gif/
#source4: #https://stackoverflow.com/questions/30223161/matplotlib-mplot3d-how-to-increase-the-size-of-an-axis-stretch-in-a-3d-plo