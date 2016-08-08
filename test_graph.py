from graphs import *

# http://www.movable-type.co.uk/scripts/latlong.html

G = {}

G["Adj"] = {"JFK":["LAX", "FCO", "CDG"],
       "LGA":["ALB","BUF", "MIA"],
       "MIA":["DFW","JFK","SLC"],
       "FCO":["OTP", "CDG", "JFK"],
       "CDG":["LGA"]}

G["E"] = {"JFKLAX":2829, 
       "JFKFCO":4264,
       "JFKCDG":3635,
       "LGAALB":161,
       "LGABUF":292,
       "LGAMIA":1100,
       "MIAJFK":1093,
       "MIADFW":1121,
       "MIASLC":2089,
       "FCOOTP":723,
       "FCOCDG":685,
       "FCOJFK":4271,
       "CDGLGA":3500}

g = Graph(G)

#g.print_adj()
#g.bfs("JFK")
g.recursive_dfs()

print g.weight("JFK", "LAX")

