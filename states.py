


def states(a):

	if(a[0] == 'A' and a[1] == 'N'):
		print "Andaman and Nicobar"
	elif(a[0] == 'A' and a[1] == 'P'):
		print "Andhra Pradesh"
	elif(a[0] == 'A' and a[1] == 'R'):
		print "Arunachal Pradesh"
	elif(a[0] == 'A' and a[1] == 'S'):
		print "Assam"
	elif(a[0] == 'B' and a[1] == 'R'):
		print "Bihar"
	elif(a[0] == 'C' and a[1] == 'G'):
		print "Chattisgarh"
	elif(a[0] == 'C' and a[1] == 'H'):
		print "Chandigarh"
	elif(a[0] == 'R' and a[1] == 'J'):
		print "Rajasthan"
	elif(a[0] == 'G' and a[1] == 'J'):
		print "Gujarat"
	elif(a[0] == 'P' and a[1] == 'B'):
		print "Punjab"
	elif(a[0] == 'H' and a[1] == 'R'):
		print "Haryana"
	elif(a[0] == 'H' and a[1] == 'P'):
		print "Himachal Pradesh"
	elif(a[0] == 'T' and a[1] == 'R'):
		print "Tripura"
	elif(a[0] == 'W' and a[1] == 'B'):
		print "West Bengal"
	elif(a[0] == 'J' and a[1] == 'K'):
		print "Jammu and Kashmir"
	elif(a[0] == 'D' and a[1] == 'D'):
		print "Daman and Diu"
	elif(a[0] == 'U' and a[1] == 'K'):
		print "Uttrakhand"
	elif(a[0] == 'K' and a[1] == 'A'):
		print "Karnataka"
	elif(a[0] == 'L' and a[1] == 'D'):
		print "Lakshwadeep"
	else:
		print "Meghalaya"

	if(a[2]%2):
		print "Odd"
		print "fine : 2000"
	else:
		print "Even"