import http.client
import json

PORT = 8000
SERVER = 'localhost'

print("\nConnecting to server: {}:{}\n".format(SERVER, PORT))

# Connect with the server
conn = http.client.HTTPConnection(SERVER, PORT)



#List of all species without limit:
conn.request("GET", "/listSpecies?limit=&json=1")
r1 = conn.getresponse()
print("Response received!: {} {}\n".format(r1.status, r1.reason))
data1 = r1.read().decode("utf-8")
response = json.loads(data1)
print (response)

#List of all species with limit:
conn.request("GET", "/listSpecies?limit=10&json=1")
r1 = conn.getresponse()
print("Response received!: {} {}\n".format(r1.status, r1.reason))
data1 = r1.read().decode("utf-8")
response = json.loads(data1)
print (response)

#Information about karyotype:
conn.request("GET", "/karyotype?specie=mouse&json=1")
r1 = conn.getresponse()
print("Response received!: {} {}\n".format(r1.status, r1.reason))
data1 = r1.read().decode("utf-8")
response = json.loads(data1)
print (response)

#Length of one chromosome:
conn.request("GET", "/chromosomeLength?specie=mouse&chromo=18&json=1")
r1 = conn.getresponse()
print("Response received!: {} {}\n".format(r1.status, r1.reason))
data1 = r1.read().decode("utf-8")
response = json.loads(data1)
print (response)

#Sequence of a given human gene:
conn.request("GET", "/geneSeq?gene=FRAT1&json=1")
r1 = conn.getresponse()
print("Response received!: {} {}\n".format(r1.status, r1.reason))
data1 = r1.read().decode("utf-8")
response = json.loads(data1)
print (response)

#Information about human gene:
conn.request("GET", "/geneInfo?gene=FRAT1&json=1")
r1 = conn.getresponse()
print("Response received!: {} {}\n".format(r1.status, r1.reason))
data1 = r1.read().decode("utf-8")
response = json.loads(data1)
print (response)

#Calculations of a given human gene:
conn.request("GET", "/geneCal?gene=FRAT1&json=1")
r1 = conn.getresponse()
print("Response received!: {} {}\n".format(r1.status, r1.reason))
data1 = r1.read().decode("utf-8")
response = json.loads(data1)
print (response)

#Names of the genes located in the chromosome from start to the end position:
conn.request("GET", "/geneList?chromo=1&start=0&end=30000&json=1")
r1 = conn.getresponse()
print("Response received!: {} {}\n".format(r1.status, r1.reason))
data1 = r1.read().decode("utf-8")
response = json.loads(data1)
print (response)

