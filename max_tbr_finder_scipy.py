
from geometry_breeder_material import *
from scipy import optimize

bnds = ((0.0,1.0),(0.0,1.0),(0.0,1.0))

result = optimize.minimize(find_tbr, [0.3,0.4,0.3], bounds=bnds)

print(result.fun)

# tbr = 1.2, enrichments =[0.2,0.4,0.5]