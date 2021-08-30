#compute the rectangles coordinates and dimensions that results as the intersection
#of two boxes.
#returns None if no intersection
def intersectionCompute(box1_x, box1_y, box1_width, box1_height, box2_x, box2_y, box2_width, box2_height):   
    leftX   = max( box1_x, box2_x );
    rightX  = min( box1_x+box1_width, box2_x+box2_width );
    topY    = max( box1_y, box2_y );
    bottomY = min( box1_y+box1_height, box2_y+box2_height );

    if leftX < rightX and topY < bottomY:
        return [leftX, topY, (rightX-leftX), (bottomY - topY)]
    else:
        return None

#compute the intersection over union (scalar float with value between 0 and 1) between
#two rectangles -> one at location (box1_x,box1_y) with dimensions (box1_width,box1_height)
#and other at location (box2_x,box2_y) with dimensions (box2_width, box2_height)
def IOU(box1_x,box1_y,box1_width,box1_height,box2_x,box2_y,box2_width,box2_height):
    intersection = intersectionCompute(box1_x,box1_y,box1_width,box1_height,box2_x,box2_y,box2_width,box2_height)
    if intersection == None:
        return 0
    
    intersection_area = intersection[2]*intersection[3]
    box1_area = box1_width * box1_height
    box2_area = box2_width * box2_height

    iou = float(intersection_area)/float(box1_area + box2_area - intersection_area)
    return iou
