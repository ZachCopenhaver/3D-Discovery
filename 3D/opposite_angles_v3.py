import csv
import os
import re
import sys
import math
import numpy as np

def get_rad_angles():
	trans_dict = {}
	with open('angles_rad.csv', mode = 'r') as inFile:
		radReader = csv.reader(inFile)
		i = 0
		for row in radReader:
			try:
				trans_dict[i] = [row[0], row[1]]
				i += 1
			except IndexError:
				break
	return trans_dict
	
def get_deg_angles():
	trans_dict = {}
	with open('angles_deg.csv', mode = 'r') as inFile:
		degReader = csv.reader(inFile)
		i = 0
		for row in degReader:
			try:
				trans_dict[i] = [row[0], row[1]]
				i += 1
			except IndexError:
				break
	return trans_dict

def pick_deg_or_rad():
	# if radians then unit = 0
	if (sys.argv[1] == 'radians'):
		trans_dict = get_rad_angles()
		return trans_dict, 0
	# if degrees then unit = 1
	elif (sys.argv[1] == 'degrees'):
		trans_dict = get_deg_angles()
		return trans_dict, 1
	else:
		return 0,2
	
def get_opposite_theta(angle, unit):
	if (unit == 0):
		return (float(angle) + math.pi) % (2*math.pi)
	elif (unit == 1):
		return (float(angle) + 180) % 360
	else:
		return 0
		
def get_opposite_phi(angle, unit):
	if (unit == 0):
		return math.pi - float(angle)
	elif (unit == 1):
		return 180 - float(angle)
	else:
		return 0
		
def get_closest(tTheta, tPhi, trans_dict):
	difference_dict = {}
	for i in range(0,35):
		diff = math.sqrt(math.pow(tTheta - float(trans_dict[i][0]),2) + math.pow(tPhi - float(trans_dict[i][1]),2))
		difference_dict[i] = diff
	min_diff = min(difference_dict.values())
	trans_num = [key for key in difference_dict if difference_dict[key] == min_diff]
	return trans_num[0]
	
# def get_row1(theta, phi, trans_dict, trans, unit):
# 	# find opposite angles
# 	tTheta = get_opposite_theta(theta, unit)
# 	tPhi = get_opposite_phi(phi, unit)
# 	
# 	# find closest angles and transceivers
# 	closest_trans = get_closest(tTheta, tPhi, trans_dict)
# 	
# 	return tTheta, tPhi, closest_trans
# 	
# def get_row2(theta, phi, trans_dict, trans, unit):
# 	if (unit == 0):
# 		tTheta = get_opposite_theta(float(theta)+math.pi, unit)
# 	elif (unit == 1):
# 		tTheta = get_opposite_theta(float(theta)+180, unit)
# 	tPhi = get_opposite_phi(phi, unit)
# 	
# 	# find closest angles and transceivers
# 	closest_trans = get_closest(tTheta, tPhi, trans_dict)
# 	
# 	return tTheta, tPhi, closest_trans
# 	
# def get_row3(theta, phi, trans_dict, trans, unit):
# 	tTheta = get_opposite_theta(theta, unit)
# 	if (unit == 0):
# 		tPhi = get_opposite_phi(float(phi)+(math.pi/4), unit)
# 	elif (unit == 1):
# 		tPhi = get_opposite_phi(float(phi)+45, unit)
# 	
# 	# find closest angles and transceivers
# 	closest_trans = get_closest(tTheta, tPhi, trans_dict)
# 	
# 	return tTheta, tPhi, closest_trans
	
def get_row1(theta, phi, trans_dict, trans, unit):
	if (unit == 0):
		tTheta = get_opposite_theta(float(theta)+math.pi, unit)
		tPhi = get_opposite_phi(float(phi)+(math.pi/4), unit)
	elif (unit == 1):
		tTheta = get_opposite_theta(float(theta)+180, unit)
		tPhi = get_opposite_phi(float(phi)+45, unit)
	
	# find closest angles and transceivers
	closest_trans = get_closest(tTheta, tPhi, trans_dict)
	
	return tTheta, tPhi, closest_trans

def get_row2(theta, phi, trans_dict, trans, unit):
	if (unit == 0):
		tTheta = get_opposite_theta(float(theta)+math.pi, unit)
		tPhi = get_opposite_phi(float(phi)+(math.pi/2), unit)
	elif (unit == 1):
		tTheta = get_opposite_theta(float(theta)+180, unit)
		tPhi = get_opposite_phi(float(phi)+90, unit)
	
	# find closest angles and transceivers
	closest_trans = get_closest(tTheta, tPhi, trans_dict)
	
	return tTheta, tPhi, closest_trans

def get_row3(theta, phi, trans_dict, trans, unit):
	if (unit == 0):
		tTheta = get_opposite_theta(float(theta)+math.pi, unit)
		tPhi = get_opposite_phi(float(phi)+(math.pi/2), unit)
	elif (unit == 1):
		tTheta = get_opposite_theta(float(theta)+180, unit)
		tPhi = get_opposite_phi(float(phi)+90, unit)
	
	# find closest angles and transceivers
	closest_trans = get_closest(tTheta, tPhi, trans_dict)
	
	return tTheta, tPhi, closest_trans

def get_row4(theta, phi, trans_dict, trans, unit):
	if (unit == 0):
		tTheta = get_opposite_theta(float(theta)+(120*math.pi/180), unit)
		tPhi = get_opposite_phi(float(phi)+(math.pi/2), unit)
	elif (unit == 1):
		tTheta = get_opposite_theta(float(theta)+120, unit)
		tPhi = get_opposite_phi(float(phi)+90, unit)
	
	# find closest angles and transceivers
	closest_trans = get_closest(tTheta, tPhi, trans_dict)
	
	return tTheta, tPhi, closest_trans

def get_row5(theta, phi, trans_dict, trans, unit):
	if (unit == 0):
		tTheta = get_opposite_theta(float(theta)-(120*math.pi/180), unit)
		tPhi = get_opposite_phi(float(phi)+(math.pi/2), unit)
	elif (unit == 1):
		tTheta = get_opposite_theta(float(theta)-120, unit)
		tPhi = get_opposite_phi(float(phi)+90, unit)
	
	# find closest angles and transceivers
	closest_trans = get_closest(tTheta, tPhi, trans_dict)
	
	return tTheta, tPhi, closest_trans

def get_row6(theta, phi, trans_dict, trans, unit):
	if (unit == 0):
		tTheta = get_opposite_theta(float(theta)-(120*math.pi/180), unit)
		tPhi = get_opposite_phi(float(phi)+(math.pi/4), unit)
	elif (unit == 1):
		tTheta = get_opposite_theta(float(theta)-120, unit)
		tPhi = get_opposite_phi(float(phi)+45, unit)
	
	# find closest angles and transceivers
	closest_trans = get_closest(tTheta, tPhi, trans_dict)
	
	return tTheta, tPhi, closest_trans

def get_row7(theta, phi, trans_dict, trans, unit):
	if (unit == 0):
		tTheta = get_opposite_theta(float(theta)-(60*math.pi/180), unit)
		tPhi = get_opposite_phi(float(phi)+(math.pi/4), unit)
	elif (unit == 1):
		tTheta = get_opposite_theta(float(theta)-60, unit)
		tPhi = get_opposite_phi(float(phi)+45, unit)
	
	# find closest angles and transceivers
	closest_trans = get_closest(tTheta, tPhi, trans_dict)
	
	return tTheta, tPhi, closest_trans

def get_row8(theta, phi, trans_dict, trans, unit):
	if (unit == 0):
		tTheta = get_opposite_theta(float(theta)-(60*math.pi/180), unit)
		tPhi = get_opposite_phi(float(phi)+(math.pi/2), unit)
	elif (unit == 1):
		tTheta = get_opposite_theta(float(theta)-60, unit)
		tPhi = get_opposite_phi(float(phi)+90, unit)
	
	# find closest angles and transceivers
	closest_trans = get_closest(tTheta, tPhi, trans_dict)
	
	return tTheta, tPhi, closest_trans

def get_row9(theta, phi, trans_dict, trans, unit):
	if (unit == 0):
		tTheta = get_opposite_theta(float(theta)-(90*math.pi/180), unit)
		tPhi = get_opposite_phi(float(phi)+(math.pi/2), unit)
	elif (unit == 1):
		tTheta = get_opposite_theta(float(theta)-90, unit)
		tPhi = get_opposite_phi(float(phi)+90, unit)
	
	# find closest angles and transceivers
	closest_trans = get_closest(tTheta, tPhi, trans_dict)
	
	return tTheta, tPhi, closest_trans

def get_row10(theta, phi, trans_dict, trans, unit):
	if (unit == 0):
		tTheta = get_opposite_theta(float(theta)-(90*math.pi/180), unit)
		tPhi = get_opposite_phi(float(phi)+(math.pi/4), unit)
	elif (unit == 1):
		tTheta = get_opposite_theta(float(theta)-90, unit)
		tPhi = get_opposite_phi(float(phi)+45, unit)
	
	# find closest angles and transceivers
	closest_trans = get_closest(tTheta, tPhi, trans_dict)
	
	return tTheta, tPhi, closest_trans
	
def write_csv(trans, trans_dict, unit):
	outFileName = ''
	if (unit == 0):
		outFileName = 'opposite_angles_rad.csv'
	elif (unit == 1):
		outFileName = 'opposite_angles_deg.csv'
	with open(outFileName, mode = 'w') as csvfile:
		out = csv.writer(csvfile)
		out.writerow(['1','Follower','','','Leader','Rotate Theta 180 Deg','Tilt 45 Deg','','',
                      '2','Follower','','','Leader','Rotate Theta 180 Deg','Tilt 90 Deg','Elevate 9 Inch','',
                      '3','Follower','','','Leader','Rotate Theta 180 Deg','Tilt 90 Deg','Elevate 6 Inch','',
                      '4','Follower','','','Leader','Rotate Theta 120 Deg','Tilt 90 Deg','Elevate 6 Inch','',
                      '5','Follower','','','Leader','Rotate Theta -120 Deg','Tilt 90 Deg','Elevate 6 Inch','',
                      '6','Follower','','','Leader','Rotate Theta -120 Deg','Tilt 45 Deg','','',
                      '7','Follower','','','Leader','Rotate Theta -60 Deg','Tilt 45 Deg','','',
                      '8','Follower','','','Leader','Rotate Theta -60 Deg','Tilt 90 Deg','Elevate 6 Inch','',
                      '9','Follower','','','Leader','Rotate Theta -90 Deg','Tilt 90 Deg','Elevate 6 Inch','',
                      '10','Follower','','','Leader','Rotate Theta -90 Deg','Tilt 45 Deg','',''])
		out.writerow(['','TxNo', 'Theta', 'Phi','Target Theta', 'Target Phi', 'Closest Theta', 'Closest Phi', 'Closest TxNo',
                      '','TxNo', 'Theta', 'Phi','Target Theta', 'Target Phi', 'Closest Theta', 'Closest Phi', 'Closest TxNo',
                      '','TxNo', 'Theta', 'Phi','Target Theta', 'Target Phi', 'Closest Theta', 'Closest Phi', 'Closest TxNo',
                      '','TxNo', 'Theta', 'Phi','Target Theta', 'Target Phi', 'Closest Theta', 'Closest Phi', 'Closest TxNo',
                      '','TxNo', 'Theta', 'Phi','Target Theta', 'Target Phi', 'Closest Theta', 'Closest Phi', 'Closest TxNo',
                      '','TxNo', 'Theta', 'Phi','Target Theta', 'Target Phi', 'Closest Theta', 'Closest Phi', 'Closest TxNo',
                      '','TxNo', 'Theta', 'Phi','Target Theta', 'Target Phi', 'Closest Theta', 'Closest Phi', 'Closest TxNo',
                      '','TxNo', 'Theta', 'Phi','Target Theta', 'Target Phi', 'Closest Theta', 'Closest Phi', 'Closest TxNo',
                      '','TxNo', 'Theta', 'Phi','Target Theta', 'Target Phi', 'Closest Theta', 'Closest Phi', 'Closest TxNo',
                      '','TxNo', 'Theta', 'Phi','Target Theta', 'Target Phi', 'Closest Theta', 'Closest Phi', 'Closest TxNo'])
		for i in range(0,35):
			# setup 1: leader is rotated 180 degrees and tilted down 45 degrees
			tTheta1, tPhi1, closest_trans1 = get_row1(trans_dict[i][0], trans_dict[i][1], trans_dict, trans, unit)
			# setup 2: leader is rotated 180 degrees, elevated 9 inches, and tilted down 90 degrees
			tTheta2, tPhi2, closest_trans2 = get_row2(trans_dict[i][0], trans_dict[i][1], trans_dict, trans, unit)
			# setup 3: leader is rotated 180 degrees, elevated 6 inches, and tilted down 90 degrees
			tTheta3, tPhi3, closest_trans3 = get_row3(trans_dict[i][0], trans_dict[i][1], trans_dict, trans, unit)
			# setup 4: leader is rotated 120 degrees, elevated 6 inches, and tilted down 90 degrees
			tTheta4, tPhi4, closest_trans4 = get_row4(trans_dict[i][0], trans_dict[i][1], trans_dict, trans, unit)
			# setup 5: leader is rotated -120 degrees, elevated 6 inches, and tilted down 90 degrees
			tTheta5, tPhi5, closest_trans5 = get_row5(trans_dict[i][0], trans_dict[i][1], trans_dict, trans, unit)
			# setup 6: leader is rotated -120 degrees, elevated 6 inches, and tilted down 45 degrees
			tTheta6, tPhi6, closest_trans6 = get_row6(trans_dict[i][0], trans_dict[i][1], trans_dict, trans, unit)
			# setup 7: leader is rotated -60 degrees and tilted down 45 degrees
			tTheta7, tPhi7, closest_trans7 = get_row7(trans_dict[i][0], trans_dict[i][1], trans_dict, trans, unit)
			# setup 8: leader is rotated -60 degrees, elevated 6 inches, and tilted down 90 degrees
			tTheta8, tPhi8, closest_trans8 = get_row8(trans_dict[i][0], trans_dict[i][1], trans_dict, trans, unit)
			# setup 9: leader is rotated -90 degrees, elevated 6 inches, and tilted down 90 degrees
			tTheta9, tPhi9, closest_trans9 = get_row9(trans_dict[i][0], trans_dict[i][1], trans_dict, trans, unit)
			# setup 10: leader is rotated -90 degrees and tilted down 45 degrees
			tTheta10, tPhi10, closest_trans10 = get_row10(trans_dict[i][0], trans_dict[i][1], trans_dict, trans, unit)
			
			out.writerow(['',trans[i], trans_dict[i][0], trans_dict[i][1], tTheta1, tPhi1, trans_dict[closest_trans1][0], trans_dict[closest_trans1][1], closest_trans1,
                          '',trans[i], trans_dict[i][0], trans_dict[i][1], tTheta2, tPhi2, trans_dict[closest_trans2][0], trans_dict[closest_trans2][1], closest_trans2,
                          '',trans[i], trans_dict[i][0], trans_dict[i][1], tTheta3, tPhi3, trans_dict[closest_trans3][0], trans_dict[closest_trans3][1], closest_trans3,
                          '',trans[i], trans_dict[i][0], trans_dict[i][1], tTheta4, tPhi4, trans_dict[closest_trans4][0], trans_dict[closest_trans4][1], closest_trans4,
                          '',trans[i], trans_dict[i][0], trans_dict[i][1], tTheta5, tPhi5, trans_dict[closest_trans5][0], trans_dict[closest_trans5][1], closest_trans5,
                          '',trans[i], trans_dict[i][0], trans_dict[i][1], tTheta6, tPhi6, trans_dict[closest_trans6][0], trans_dict[closest_trans6][1], closest_trans6,
                          '',trans[i], trans_dict[i][0], trans_dict[i][1], tTheta7, tPhi7, trans_dict[closest_trans7][0], trans_dict[closest_trans7][1], closest_trans7,
                          '',trans[i], trans_dict[i][0], trans_dict[i][1], tTheta8, tPhi8, trans_dict[closest_trans8][0], trans_dict[closest_trans8][1], closest_trans8,
                          '',trans[i], trans_dict[i][0], trans_dict[i][1], tTheta9, tPhi9, trans_dict[closest_trans9][0], trans_dict[closest_trans9][1], closest_trans9,
                          '',trans[i], trans_dict[i][0], trans_dict[i][1], tTheta10, tPhi10, trans_dict[closest_trans10][0], trans_dict[closest_trans10][1], closest_trans10])
	
	
# trans is the list of keys for trans_dict
trans = []
for i in range(0,35):
	trans.append(i)
# trans_dict is a map where key = transceiver number and value = [theta, phi]
trans_dict, unit = pick_deg_or_rad()
if (unit == 0 or unit == 1):
	write_csv(trans, trans_dict, unit)


