import http.server

import socketserver

import termcolor

import json

import http.client

from Seq import Seq



# Define the Server's port

PORT = 8000



# It means that our class inheritates all his methods and properties

class TestHandler(http.server.BaseHTTPRequestHandler):



    def arguments_fuction (self, path):

        dictionary = dict()  #Dictionary with parameters

        if '?' in path:

            argumentos = path.split('?')[1]

            argumentos = argumentos.split(" ")[0]

            cuts = argumentos.split('&')

            for partner in cuts: #Loop for obtain the parameters

                if '=' in partner:

                    key=partner.split("=")[0]

                    value=partner.split("=")[1]

                    dictionary[key]=value

        return dictionary







    def do_GET(self):

        response_code = 200

        json_response=False

        #This method is called whenever the client invokes the GET method in the HTTP protocol request





        # Print the request line

        termcolor.cprint(self.requestline, 'green')


        # Different endpoints.

        if self.path == "/" or self.path == "/index.html":

            with open("index.html", "r") as f:

                contents = f.read()

        elif "/listSpecies" in self.path:

            argumentos = self.arguments_fuction(self.path)

            if 'limit' in argumentos:

                try:

                    limit=int(argumentos['limit'])

                except:

                    limit=0

            else:

                limit=0

            if limit!=0: #LIMIT LIST

                #cut = (self.path).split("=")

                limit = argumentos['limit'] #cut[1]

                print("LIMIT:",limit)

                conn = http.client.HTTPConnection("rest.ensembl.org")

                conn.request("GET", "/info/species?content-type=application/json")

                r1 = conn.getresponse()

                print()

                print("Response received: ", end='')

                print(r1.status, r1.reason)

                text_json = r1.read().decode("utf-8")

                response = json.loads(text_json)

                conn.close()

                list_species = response['species']

                if 'json' in argumentos:  #Json response.

                    json_response=True

                    new_list =list_species[1:int(limit)]

                    contents=json.dumps(new_list)



                else: #Response without json.

                    contents="""

                        <html>

                        <body style= "background-color: orange;">

                        <u><font face="Impact">THIS IS THE LIST OF SPECIES YOU HAVE REQUESTED:</font></u>

                        <ol>"""

                    counter = 0

                    for specie in list_species:

                        contents=contents+"<li>"+specie['display_name']+"</li>"

                        counter = counter + 1

                        if counter == int(limit) :

                            break



                    contents= contents+"""</ol>

                        </body>

                        </html>

                    """



            else: #ALL LIST.

                conn = http.client.HTTPConnection("rest.ensembl.org")

                conn.request("GET","/info/species?content-type=application/json")  # returns the list of all species

                r1 = conn.getresponse()

                print()

                print("Response received: ", end='')

                print(r1.status, r1.reason)

                text_json = r1.read().decode("utf-8")

                response = json.loads(text_json)

                conn.close()

                list_species = response['species']

                if 'json' in argumentos: #Json response.

                    json_response=True

                    contents=json.dumps(list_species)

                else:  #Response without json.

                    contents = """

                                    <html>

                                    <body style= "background-color: orange;">

                                    <u><font face="Impact">THIS IS THE LIST OF ALL SPECIES</font></u>

                                    <ol>"""

                    for specie in list_species:

                        contents = contents + "<li>" + specie['display_name'] + "</li>"



                    contents = contents + """</ol>

                                    </body>

                                    </html>

                                """



        elif "/karyotype" in self.path:

            argumentos = self.arguments_fuction(self.path)

            if 'specie' in argumentos and argumentos['specie']!="":

                specie = argumentos['specie']

                try:

                    conn = http.client.HTTPConnection("rest.ensembl.org")

                    conn.request("GET", "/info/assembly/" + specie + "?content-type=application/json")

                    r1 = conn.getresponse()

                    data1 = r1.read().decode("utf-8")

                    response = json.loads(data1)

                    list_chromo = response["karyotype"]

                    #print(list_chromo)



                    if 'json' in argumentos: #Json response

                        json_response=True

                        print(list_chromo)

                        contents = json.dumps(list_chromo)

                    else: #Response without json.

                        contents = """

                                                    <html>

                                                    <body style= "background-color: orange;">

                                                    <u><font face="Impact">THIS IS THE LIST OF SPECIES YOU HAVE REQUESTED:</font></u>

                                                    <ul>"""

                        for chromo in list_chromo:

                            contents = contents + "<li>" + chromo + "</li>"



                        contents = contents + """</ul>

                                                                    </body>

                                                                    </html>

                                                                """

                except ValueError: #Some error

                    response_code = 400

                    f = open("error.html", 'r')

                    contents = f.read()

                except KeyboardInterrupt:

                    response_code = 400

                    f = open("error.html", 'r')

                    contents = f.read()

                except KeyError:

                    response_code = 400

                    f = open("error.html", 'r')

                    contents = f.read()

                except NameError:

                    response_code = 400

                    f = open("error.html", 'r')

                    contents = f.read()



            else:

                response_code = 400

                f = open("error.html",'r')

                contents = f.read()

        elif "/chromosomeLength" in self.path:

            argumentos=self.arguments_fuction(self.path)

            if ('specie' in argumentos and 'chromo' in argumentos) and (argumentos['specie'] != "" and argumentos['chromo']!=""):

                chromo= argumentos['chromo']

                print(chromo)

                specie = argumentos['specie']

                print(specie)

                try: #Connection

                    conn = http.client.HTTPConnection("rest.ensembl.org")

                    conn.request("GET", "/info/assembly/" + specie + "?content-type=application/json")

                    r1 = conn.getresponse()

                    data1 = r1.read().decode("utf-8")

                    response = json.loads(data1)

                    info = response["top_level_region"]

                    length = 0

                    if 'json' in argumentos:  #Json response.

                        json_response=True

                        for element in info:

                            if element["name"] == chromo:

                                length = element["length"]

                        print(length)

                        contents = json.dumps(length)
                        if length == 0:
                            response_code = 400

                            f = open("error.html", 'r')

                            contents = json.dumps(f.read())

                    else: #Response without json.

                        contents = """

                                        <html>

                                        <body style= "background-color: orange;">

                                        <u><font face="impact">THIS IS THE LENGTH OF THE CHROMOSOME OF THE SPECIES THAT YOU HAVE REQUESTED</font></u>

                                        <ul>"""

                        for element in info:

                            if element["name"]==chromo:

                                length = element["length"]

                        #print(length)

                        contents = contents + "<li>" + str(length) + "</li>"

                        contents = contents + """</ul>

                                                                    </body>

                                                                    </html>

                                                                """
                        if length == 0: #This is an error, it does not exist.
                            response_code = 400

                            f = open("error.html", 'r')

                            contents = f.read()


                except ValueError:

                    response_code = 400

                    f = open("error.html", 'r')

                    contents = f.read()

                except KeyboardInterrupt:

                    response_code = 400

                    f = open("error.html", 'r')

                    contents = f.read()

                except KeyError:

                    response_code = 400

                    f = open("error.html", 'r')

                    contents = f.read()

                except NameError:

                    response_code = 400

                    f = open("error.html", 'r')

                    contents = f.read()



            else:

                response_code = 400

                f = open("error.html", 'r')

                contents = f.read()





        elif "/geneSeq" in self.path:

            argumentos = self.arguments_fuction(self.path)

            if 'gene' in argumentos and argumentos['gene']!="":

                gene = argumentos['gene']

                try: #Connection.

                    conn = http.client.HTTPConnection("rest.ensembl.org")

                    conn.request("GET", "/homology/symbol/human/"+gene+"?content-type=application/json")

                    r1 = conn.getresponse()

                    data1 = r1.read().decode("utf-8")

                    response = json.loads(data1)

                    id = response['data'][0]['id']

                    conn.request("GET", "/sequence/id/"+id+"?content-type=application/json")

                    r1 = conn.getresponse()

                    data1 = r1.read().decode("utf-8")

                    response = json.loads(data1)

                    cadena = response['seq']

                    if 'json' in argumentos: #Json response.

                        json_response=True

                        print(cadena)

                        contents=json.dumps(cadena)

                    else: #Response without json. #Creating a html

                        contents = """      

                                        <html>

                                        <body style= "background-color: orange;">

                                        <u><font face="impact">SEQUENCE OF A GIVEN HUMAN GENE</font></u>

                                        <ul>"""+cadena+"""</ul>

                                                                                </body>

                                                                                </html>

                                                                            """

                except ValueError:

                    response_code = 400

                    f = open("error.html", 'r')

                    contents = f.read()

                except KeyboardInterrupt:

                    response_code = 400

                    f = open("error.html", 'r')

                    contents = f.read()

                except KeyError:

                    response_code = 400

                    f = open("error.html", 'r')

                    contents = f.read()

                except NameError:

                    response_code = 400

                    f = open("error.html", 'r')

                    contents = f.read()

            else:

                response_code = 400

                f = open("error.html", 'r')

                contents = f.read()







        elif "/geneInfo" in self.path:

            argumentos = self.arguments_fuction(self.path)

            if 'gene' in argumentos and argumentos['gene'] != "":

                gene = argumentos['gene']  #looking in the dictionary.

                try:

                    conn = http.client.HTTPConnection("rest.ensembl.org")

                    conn.request("GET", "/homology/symbol/human/" + gene + "?content-type=application/json")

                    r1 = conn.getresponse()

                    data1 = r1.read().decode("utf-8")

                    response = json.loads(data1)

                    id = response['data'][0]['id']

                    conn.request("GET", "/overlap/id/"+id+"?feature=gene;content-type=application/json")

                    r1 = conn.getresponse()

                    data1 = r1.read().decode("utf-8")

                    response = json.loads(data1)

                    start = response[0]['start']

                    end = response[0]['end']



                    length = end - start  #Calculating the final lenght.

                    chromo = response[0]['seq_region_name']

                    if 'json' in argumentos: #Json response

                        json_response=True

                        contents=[id, start,end,length,chromo]

                        contents=json.dumps(contents)

                    else: #Response without json.



                        contents = """

                                                    <html>

                                                    <body style= "background-color: orange;">

                                                    <u><font face="impact">THE ID OF THE GENE:</font></u>

                                                    <ul>""" + str(id) + """</ul>

                                                    <u><font face="impact">START:</font></u>

                                                    <ul>""" + str(start) + """</ul>

                                                    <u><font face="impact">END:</font></u>

                                                    <ul>""" + str(end) + """</ul>

                                                    <u><font face="impact">THE LENGTH:</font></u>

                                                    <ul>""" + str(length) + """</ul>

                                                    <u><font face="impact">THE CHROMOSOME:</font></u>

                                                    <ul>""" + chromo + """</ul>

                                                                                            </body>

                                                                                            </html>

                                                                                        """

                except ValueError:

                    response_code = 400

                    f = open("error.html", 'r')

                    contents = f.read()

                except KeyboardInterrupt:

                    response_code = 400

                    f = open("error.html", 'r')

                    contents = f.read()

                except KeyError:

                    response_code = 400

                    f = open("error.html", 'r')

                    contents = f.read()

                except NameError:

                    response_code = 400

                    f = open("error.html", 'r')

                    contents = f.read()

            else:

                response_code = 400

                f = open("error.html", 'r')

                contents = f.read()



        elif "/geneCal" in self.path:

            argumentos = self.arguments_fuction(self.path)

            if 'gene' in argumentos and argumentos['gene'] != "":

                gene = argumentos['gene'] #looking for the key word at the dicctionary.

                try:

                    conn = http.client.HTTPConnection("rest.ensembl.org")

                    conn.request("GET", "/homology/symbol/human/" + gene + "?content-type=application/json")

                    r1 = conn.getresponse()

                    data1 = r1.read().decode("utf-8")

                    response = json.loads(data1)

                    id = response['data'][0]['id']

                    conn.request("GET", "/sequence/id/" + id + "?content-type=application/json")

                    r1 = conn.getresponse()

                    data1 = r1.read().decode("utf-8")

                    response = json.loads(data1)

                    cadena = response['seq']

                    s1 = Seq(cadena)

                    longitud = len(cadena)

                    percA = s1.perc('A')

                    percT = s1.perc('T')

                    percC = s1.perc('C')

                    percG = s1.perc('G')

                    if 'json' in argumentos: #Json response.

                        json_response=True

                        contents=[longitud, percA, percT, percC, percG]

                        contents=json.dumps(contents)

                    else: #Response without json.

                        contents = """

                                                                <html>

                                                                <body style= "background-color: orange;">

                                                                <u><font face="impact">LENGTH:</font></u>

                                                                <ul>""" + str(longitud) + """</ul>

                                                                <u><font face="impact">PERCA:</font></u>

                                                                <ul>""" +str(percA)  + """</ul>

                                                                <u><font face="impact">PERCT:</font></u>

                                                                <ul>""" + str(percT) + """</ul>

                                                                <u><font face="impact">PERCG:</font></u>

                                                                <ul>""" + str(percG) + """</ul>

                                                                <u><font face="impact">PERCC:</font></u>

                                                                <ul>""" + str(percC) + """</ul>

                                                                                                        </body>

                                                                                                        </html>

                                                                                                    """

                except ValueError:

                    response_code = 400

                    f = open("error.html", 'r')

                    contents = f.read()

                except KeyboardInterrupt:

                    response_code = 400

                    f = open("error.html", 'r')

                    contents = f.read()

                except KeyError:

                    response_code = 400

                    f = open("error.html", 'r')

                    contents = f.read()

                except NameError:

                    response_code = 400

                    f = open("error.html", 'r')

                    contents = f.read()

            else:

                response_code = 400

                f = open("error.html", 'r')

                contents = f.read()



        elif "/geneList" in self.path:

            argumentos = self.arguments_fuction(self.path)

            if ('chromo' in argumentos and 'start' in argumentos and 'end' in argumentos) and (argumentos['chromo'] != "" and argumentos['start'] != "" and argumentos['end'] != "") :

                chromo = argumentos['chromo']

                start = argumentos['start']

                end = argumentos['end']



                print(end)

                try: #Connection.

                    conn = http.client.HTTPConnection("rest.ensembl.org")

                    conn.request("GET", "/overlap/region/human/" + str(chromo) + ":" + str(start) + "-" + str(

                    end) + "?content-type=application/json;feature=gene;feature=transcript;feature=cds;feature=exon")

                    r1 = conn.getresponse()

                    data1 = r1.read().decode("utf-8")

                    response = json.loads(data1)

                    print(response)

                    if 'json' in argumentos: #Json reponse.

                        json_response = True

                        lista=[]

                        for i in response:

                            if (i['feature_type'] == "gene"):



                                lista.append([i['external_name'],i['start'],i['end']])

                        contents=json.dumps(lista)

                    else: #Response without json.

                        contents = """<html>

                                    <head>

                                        <title>FINAL PRACTICE</title>

                                        <body style= "background-color: orange;">

                                    </head>

                                    <baby>

                                        <ul>"""

                        for i in response: #loop

                            if (i['feature_type']=="gene"):

                                contents= contents+"<li>"+(str(i['external_name'])+" "+str(i['start'])+" "+str(i['end']))+"</li>"

                        contents = contents+"""</ul></body></html>"""

                except ValueError:

                    response_code = 400

                    f = open("error.html", 'r')

                    contents = f.read()

                except KeyboardInterrupt:

                    response_code = 400

                    f = open("error.html", 'r')

                    contents = f.read()

                except KeyError:

                    response_code = 400

                    f = open("error.html", 'r')

                    contents = f.read()

                except NameError:

                    response_code = 400

                    f = open("error.html", 'r')

                    contents = f.read()

                except TypeError:

                    response_code = 400

                    f = open("error.html", 'r')

                    contents = f.read()



            else:

                response_code = 400

                f = open("error.html", 'r')

                contents = f.read()



        else:

            response_code = 404

            with open("error.html", "r") as f:

                contents = f.read()



        # Generating the response message



        self.send_response(response_code)



        if json_response:

            self.send_header('Content-Type','application/json')

        else:

            self.send_header('Content-Type', 'text/html')



        self.send_header('Content-Length', len(str.encode(contents)))



        # The header is finished

        self.end_headers()



        # Send the response message

        self.wfile.write(str.encode(contents))



        return




# -- Set the new handler

Handler = TestHandler

socketserver.TCPServer.allow_reuse_address = True



# -- Open the socket server

with socketserver.TCPServer(("", PORT), Handler) as httpd:



    print("Serving at PORT", PORT)



# -- Main loop: Attend the client. Whenever there is a new

# -- clint, the handler is called

    try:

        httpd.serve_forever()

    except KeyboardInterrupt:

        print(" ")

        print("Stoped by the user")

        httpd.server_close()



    print("")

    print("Server Stopped")