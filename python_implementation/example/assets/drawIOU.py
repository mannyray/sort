import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import glob
import os
import sys
sys.path.insert(0,'..')
import intersection

width = 500
height = 500

rec_width = 200
rec_height = 300
first_x = 50
second_x = first_x + rec_width + 10

counter = 0
while second_x > first_x: 
    print(counter)

    image = Image.new( 'RGB', ( width, height ) )
    draw = ImageDraw.Draw(image)
    draw.rectangle ((0,0,width,height), fill = (255,255,255) )
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)
    
    IOU = round(intersection.IOU(first_x,100,rec_width,rec_height,second_x,100,rec_width,rec_height),3)

    draw.text((first_x+rec_width/2,100+rec_height+10),"IOU="+str(IOU),fill=(0,0,0), font=font)

    im = np.array( image ) 

    # Create figure and axes
    fig,ax = plt.subplots(1)

    # Display the image
    ax.imshow(im)

    # Create a Rectangle patch
    rect = patches.Rectangle((first_x,100),rec_width,rec_height,linewidth=1,edgecolor='r',facecolor='none')

    # Add the patch to the Axes
    ax.add_patch(rect)

    rect = patches.Rectangle((second_x,100),rec_width,rec_height,linewidth=1,edgecolor='b',facecolor='none')

    # Add the patch to the Axes
    ax.add_patch(rect)

    plt.axis('off')
    plt.savefig('tmp'+str(counter).zfill(3))
    plt.close()

    second_x = second_x - 1
    counter = counter + 1

fp_in = "tmp*.png"
fp_out = os.path.join("assets","iou_example.gif")
img, *imgs = [Image.open(f) for f in sorted(glob.glob(fp_in))]
img.save(fp=fp_out, format='GIF', append_images=imgs,save_all=True, duration=10, loop=0)

[os.remove(f) for f in sorted(glob.glob(fp_in))]
