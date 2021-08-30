import sys
sys.path.insert(0,'..')
import intersection

result = intersection.IOU(1,1,4,9,2,5,5,10)
assert( abs(result - 15.0/(36 + 50 - 15.0)) < 0.000001 )
