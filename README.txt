README for main_Marquez_Viz.py

This script outputs a .GIF file that overlays the last 10 strikeout pitches of Marquez's 2021 season onto Coors Field.

A brief 'query' from the pitch_data_2021.csv by Pitcher == 'Marquez, German', and the tail(n=10) of KorBB == 'Strikeout' was run
to create the Marquez_last10Ks.csv to avoid having to read in the large, full season package each time. 

This file contains Pitcher, Batter, TaggedPitchType, PitchCall, KorBB, RelSpeed, VertBreak, HorzBreak, x0, y0, and z0
columns, with an addition 'YBreak' column inserted being the distance the ball traveled to the plate.

The main_Marquez_script iterates through each pitch and creates a pitch_path dataframe that contains ten points along the 
pitch's trajectory. Note that y axis is incremented linearlly like time, whereas x and z axis are incremented by a ^2 value
because pitch break is caused by an acceleration (or force/mass).

After generating the path of the ball, the scrip then generates a figure for each stage of the flight path, incrementing to 
show the balls position over time. Additional information such as the pitcher's name, the pitch type and velocity, as well as
the batter and how they struck out is displayed over the figure. Ten pitches and ten figures per pitch results in 100 .png files.

At the end of the script is where the .GIF is generated. It reads in all of the newly created .png files of the ball path and 
lays them over the image of Coors field. The flight path figures had to be oriented and shifted to align with the Coors picture.
*Note: I have tried the script on two computers and the image shift (line 115) was different on each to get them to align.

This was an awesome project for me, I learned how to work with .PNG and how to create .GIF files with PIL library to make a rough
version of a pitch trax.