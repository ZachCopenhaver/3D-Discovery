# Setup 3D Matplotlib projection
import math
import random
from fractions import Fraction
from mpl_toolkits import mplot3d
from matplotlib import cm
#%matplotlib inline
import numpy as np
import matplotlib.pyplot as plt
# fig = plt.figure()
# ax = plt.axes(projection='3d')

# Define constants and variables
# beta = np.pi / 8 # Define β in radians
rad = 1.0 # Define radius
cone_height = 2.5 # Arbitrary height to draw cone to
num_iterations = 1000 # The number of times to loop the simulation for a given β value
max_attempts = 1000 # The number of times to randomly pick two cones before giving up without picking two facing ones

# Construct the sphere
# ax.set_xlabel('X')
# ax.set_ylabel('Y')
# ax.set_zlabel('Z')
# ax.set_xlim(-2,2)
# ax.set_ylim(-2,2)
# ax.set_zlim(0,4)

# u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
# x = np.cos(u)*np.sin(v)
# y = np.sin(u)*np.sin(v)
# z = np.cos(v)
#ax.plot_wireframe(x, y, z, color="r", alpha=0.75)

# Draw a single cone
def draw_cone(beta, phi):
    theta_vals = np.linspace(0, 2*np.pi, 100)
    phi_vals = np.linspace(0, np.pi + (math.sqrt(2) * beta), 100)
    r = np.linspace(0, rad, 100)
    t,R =np.meshgrid(theta_vals, r)

    X = R*np.cos(t) * np.cos(beta) * np.sin(phi_vals)
    Y = R*np.sin(t) * np.cos(beta) * np.sin(phi_vals)
    Z = R*cone_height * np.cos(beta) * np.cos(phi_vals)
    
    ax.plot_surface(X, Y, Z,alpha=0.8, cmap=cm.copper)
    
def draw_cones(beta):
    beta_str = "(" + str(Fraction(beta_frac).limit_denominator()) + ")π"
    ax.set_title("β = " + beta_str)
    theta_arr = [0] # Array of θ
    for phi in np.arange(0, np.pi + (math.sqrt(2) * beta), (math.sqrt(2) * beta)):
        if phi == 0:
            continue
        else:
            n_phi = math.ceil( (2 * np.pi * rad * math.sin(phi)) / (math.sqrt(2) * beta) )
            for j in range(0, n_phi):
                theta = j * ( (2 * np.pi) / n_phi )
                theta_arr.append( theta )
            #draw_cone(beta, phi)
    #draw_cone(beta, theta_arr, phi)

# Convert θ and φ values to X, Y, and Z values for the purposes of drawing the cones
def to_cartesian(beta, theta, phi):
    x = rad * np.cos(beta) * np.sin(phi) * np.cos(theta)
    y = rad * np.cos(beta) * np.sin(phi) * np.sin(theta)
    z = rad * np.cos(beta) * np.cos(phi)
    return (x, y, z)


# Generate the θ and φ values
def get_theta_phi(beta):
    arr = [(0, 0)] # Array of θ and φ
    for phi in np.arange(0, np.pi + (math.sqrt(2) * beta), (math.sqrt(2) * beta)):
        if phi == 0:
            continue
        else:
            n_phi = math.ceil( (2 * np.pi * rad * math.sin(phi)) / (math.sqrt(2) * beta) )
            for j in range(0, n_phi):
                theta = j * ( (2 * np.pi) / n_phi )
                arr.append( (theta, phi) )
    return arr

# Generate the X, Y, and Z values
def get_xyz(beta):
    arr2 = [(0, 0, 0)] # Array of X, Y, and Z
    arr2.pop()
    for theta_phi in get_theta_phi(beta):
        xyz = to_cartesian(beta, theta_phi[0], theta_phi[1])
        arr2.append(xyz)
    return arr2
 
def calculate_angle(x1, y1, z1, 

                   x2, y2, z2,

                   x3, y3, z3):

                        

    # Find direction ratio of line AB

    ABx = x1 - x2;

    ABy = y1 - y2;

    ABz = z1 - z2;
 

    # Find direction ratio of line BC

    BCx = x3 - x2;

    BCy = y3 - y2;

    BCz = z3 - z2;
 

    # Find the dotProduct

    # of lines AB & BC

    dotProduct = (ABx * BCx +

                  ABy * BCy +

                  ABz * BCz);
 

    # Find magnitude of

    # line AB and BC

    magnitudeAB = (ABx * ABx +

                   ABy * ABy +

                   ABz * ABz);

    magnitudeBC = (BCx * BCx +

                   BCy * BCy +

                   BCz * BCz);
 

    # Find the cosine of

    # the angle formed

    # by line AB and BC

    angle = dotProduct;

    angle /= math.sqrt(magnitudeAB *

                       magnitudeBC);
 

    # Find angle in radian

    #angle = (angle * 180) / 3.14;
    return angle
 

    
def is_facing(A, coneA, B, beta, r):
    Xc = A[0] + r * np.sin(coneA[0]) * np.cos(coneA[1])
    Yc = A[1] + r * np.sin(coneA[0]) * np.sin(coneA[1])
    Zc = A[2] + r * np.cos(coneA[0])
    
    C = (Xc, Yc, Zc)
    
    angle = calculate_angle(C[0], C[1], C[2], A[0], A[1], A[2], B[0], B[1], B[2])
    
    return angle <= beta
    

# #draw_cones(beta)
# beta_vals = list()
# beta_labels = list()
# box_vals = list()
# num_cones = list()
# for beta_deg in range(5, 45):    
    # attempt_vals = list()
beta_deg=25
beta_frac = beta_deg / 180
beta = beta_deg * (np.pi / 180)
cone_theta_phi = get_theta_phi(beta)
print("Number of cones required = " + str(len(cone_theta_phi)))


cone_th_phi_degree = [(th*180/np.pi,phi*180/np.pi) for (th,phi) in cone_theta_phi]

print("The list of theta and Phi in radian are"+ str(cone_theta_phi))

print("The list of theta and Phi in degreee are"+ str(cone_th_phi_degree))

    # cone_centre_points = get_xyz(beta)
#     beta_str = "(" + str(Fraction(beta_frac).limit_denominator()) + ")π"
#     #print("\nβ is " + beta_str + " and yields " + str(len(cone_centre_points)) + " cones:")
#     #print("\t" + str(cone_centre_points) + "\n")

#     for itr in range(0, num_iterations):
#         num_attempts = 0 # Number of attempts needed to get two randomly selected cones that face one another
        
#         # X, Y, Z
#         A = (random.uniform(0, 10), random.uniform(0, 10), random.uniform(0, 10))
#         B = (random.uniform(0, 10), random.uniform(0, 10), random.uniform(0, 10))
        
#         for attempt in range(0, max_attempts):
#             # Select two random cones
#             #print(len(cone_theta_phi))
#             coneA_index = random.randint(0, len(cone_theta_phi) - 1)
#             coneB_index = random.randint(0, len(cone_theta_phi) - 1)
#             #print(coneA_index)
#             #print(coneB_index)
#             coneA = cone_theta_phi[coneA_index]
#             coneB = cone_theta_phi[coneB_index]

#             # Determine if two cones are facing one another
#             both_facing = is_facing(A, coneA, B, beta, rad) and is_facing(B, coneB, A, beta, rad)
            
#             #is_facing = random.randint(0, 2) == 1
#             if both_facing:#is_facing:
#                 num_attempts = attempt
#                 break
#             else:
#                 num_attempts = attempt

#         # Output results of iterations
#         #print("Iteration " + str(itr) + ": With a β of " + beta_str + ", it took " + str(num_attempts) + " attempt(s) to get two randomly facing, matching cones. There were a maximum of " + str(max_attempts) + " allowed attempt(s).")
#         attempt_vals.append(num_attempts)
#     beta_vals.append(beta_deg)
#     beta_labels.append(str(beta_deg) + "°")
#     box_vals.append(attempt_vals)
#     num_cones.append(len(cone_centre_points))
    
#     # Output information for all cones
#     #for coords in cone_centre_points:
#         #print("\t" + str(coords)) # Cone coordinates
#         #draw_cone(coords[0], coords[1], coords[2]) # Visual representation of cone
# fig1, ax1 = plt.subplots()
# ax1.set_title('Discovery Time per β Value')
# ax1.set_xlabel('β°')
# ax1.set_ylabel('Discovery Time')
# fig1.set_size_inches(18.5, 10.5, forward=True)
# ax1.boxplot(box_vals, labels=beta_labels, patch_artist=True)

# fig2, ax2 = plt.subplots()
# ax2.set_title('Number of Cones per β Value')
# ax2.set_xlabel('β°')
# ax2.set_ylabel('Number of Cones')
# ax2.stem(beta_vals, num_cones)

#print(beta_vals)
#print(box_vals)
#print(num_cones)

# Draw cone
# theta = np.linspace(0, 2*np.pi, 100)
# r = np.linspace(0, 2, 100)
# t,R =np.meshgrid(theta, r)
# X = R*np.cos(t)
# Y = R*np.sin(t)
# Z = R*0.75
