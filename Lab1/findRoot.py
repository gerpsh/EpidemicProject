#/usr/bin/python

#Determines source of infection form epidemic lab data.


#wasInfected function tests whether an id passed to it was infected by the end of Round 1
def wasInfected(iid):
    ifile = open('Round1Infections.csv')
    line = ifile.readline()
    idList = []
    while line != '':
        idList.append(int(line))
        line = ifile.readline()
    ifile.close()
    if iid in idList:
        return True
    else:
        return False


import individual

classSize = 16
#opens data files;
#shakes.csv contains all contacts in order of occurrence
#infects.csv contains list of all indivuals who were infected after contact

shakesFile = open('shakes.csv')
infectsFile = open('infections.csv')

#masterDict is a hashtable that contains 'individual' objects with their ids as their keys
masterDict = {}

#fills masterDict with generic 'individual' objects and assign a key that matches their ids

for i in range(1, (classSize + 1)):
    indiv = individual.Individual(i)
    indiv.contacts.append(i) #add own id to list of contacts
    masterDict[i] = indiv

#Reads 'shakes' file, see file for structure
#After each line is read, the 'contact' list of each individual in line is appended to the other's

line = shakesFile.readline()
while line != '':
    members = line.split(',')
    memberOne = int(members[0])
    memberTwo = int(members[1])

    indiv1 = masterDict[memberOne]
    indiv2 = masterDict[memberTwo]

    indiv1.addContacts(indiv2.contacts)
    indiv2.addContacts(indiv1.contacts)

    masterDict[memberOne] = indiv1
    masterDict[memberTwo] = indiv2
    
    line = shakesFile.readline()

#constructs separate hashtable containing individuals who were found to be infected at the end with their id as the key
infectedDict = {}

line = infectsFile.readline()
while line != '':
    infectee = int(line)
    infectedIndiv = masterDict[infectee]
    infectedIndiv.infected = True
    infectedDict[infectee] = infectedIndiv

    line = infectsFile.readline()

#removes duplicate values from each contact list of infected individuals, or 'set' each list, and add each set to new list 
setList = []
for key in infectedDict.iterkeys():
    setList.append(set(infectedDict[key].contacts))


    
shakesFile.close()
infectsFile.close()

#prints all individual ids and their contact set
#for i in range(1, (classSize + 1)):
#    print(str(i) + ': ' + str(set(masterDict[i].contacts)))

#find intersection of each set, which is the set of individuals that have made contact with all infected individuals; this idicates an initial set of possible origins
u = set.intersection(*setList)

#if a member of the set above is not infected by the end of the set, it is not a possible origin, and a new set ('u') is constructed with only infected individual ids
cutSet = set()
for eachId in u:
    if eachId in infectedDict:
        cutSet.add(eachId)
u = cutSet
#print(u)


#if an individual in set u made contact with someone who was not infected by the end of round 1, then that individual is no longer a candidate,
#and is removed from the set; this is the extent to which we can draw conclusions on the data, and if the origin can be determined, this will yield
#the origin
round1Shakes = open('Round1Shakes.csv')
line = round1Shakes.readline()
while line != '':
    pair = line.split(',')
    one = pair[0]
    two = pair[1]
    #print(str(pair[0]) + ' ' + str(wasInfected(int(pair[0]))))

    if int(pair[0]) in u:
        if not wasInfected(int(pair[1])):
            u.remove(int(pair[0]))
    elif int(pair[1]) in u:
        if not wasInfected(int(pair[0])):
            u.remove(int(pair[1]))
    
    #for iid in pair:
    #    if not wasInfected(int(iid)) and int(iid) in u:
    #        u.remove(int(iid))
    
    line = round1Shakes.readline()
            
round1Shakes.close()

print(u)



