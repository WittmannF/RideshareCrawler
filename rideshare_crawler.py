"""
This code tries to understand routes, dates and types of offers from posts of 
rideshare foruns. For example the following post:

"Offering: SLO to San Diego 
Tomorrow Thursday 5/26 
leaving around 6 or 7pm 
Requesting $20 for gas 
Message me if you need a ride!"

Will return the following information: post_type = 'offering' from_city = 'sd' 
to_city = 'slo'

The ultimate goal is to serve as backend tool to identify any kind of post from 
rideshare foruns. The next steps in the given code are to find bugs, to 
consider posts when someone post a trip back and to understand the dates.

This code is initially using simple solutions, whenever they are enough to solve
the problems, later, if necessary, Machine Learning tools such as text
classification might be used. 

"""

def it_has(words, post):
	for word in words:
		if word.lower() in post.lower():
			return True
	return False

def where(words, post):
    position = list()
    n = 0
    for word in words:
        for c in range(0,len(post)-len(word)):
            if post[c:c+len(word)].lower() == word.lower():
                if c not in position and c-1 not in position and c+1 not in position: #necessary because of possible spaces before and after keyword
                    position.append(c)
                    n = n + 1
    if n > 1:
        print 'I found the same city more than once'
        return position
    if n == 0:
        print 'could not find the city'
        return -1
    return position

def get_type(post):
  if "seeking" in post.lower():
    return "seeking"
  elif "offering" in post.lower():
    return "offering"
  elif "seek" in post.lower(): # this way it will prioritize the complete word
    return "seeking"
  elif "offer" in post.lower():
    return "offering"
  return "unknown"

def get_route(post): # tries to get the origin and destination of the desired trip
    # here I will investigate which cities where found in the post, and how many times the same city 
    SF = ['sf', ['san francisco', 'sf', 'bay', 'sj', 'san jose']]
    SLO = ['slo', ['slo','san luis obispo']]
    LA = ['la', [' la','la ', 'los angeles']]
    SD = ['sd', [' sd','sd ', 'san diego']]
    SAC = ['sac', ['sac', 'sacramento']]
    
    cities_dict = [SF, SLO, LA, SD, SAC]
    city = list()
    loc = list()
    n = 0 # number of found cities, if n = 1, it will be assumed that one of the cities is SLO
    for kws in cities_dict: # for each set of keywords of each city
        if it_has(kws[1], post): # if it has one of the keywords
            n = n + 1            
            city.append(kws[0]) # then append the name of the city
            position = where(kws[1], post) # also save the position, which might be a set
            if len(position) > 1:
                print 'same city found '
                print len(position)
                print 'times, I will append only the first position, please check:'
                print position                
                print post
                loc.append(position[0])
            else:
                loc.append(position[0])
# in the end I have the number of different cities (n), their location (loc) and their names (city)

# now I will decide the from_city and the to_city based on the number of cities found
    if n == 0:
        print 'no cities found for post, try to update dictionary: ' 
        print post
    if n == 1: # if only one city found, either from is SLO or one of the cities is not in the dict
        print 'only one city was found, assuming from = SLO, please check the post: '
        print post
        from_city = 'slo'
        to_city = city[0]
    if n == 2:
        if loc[0] < loc[1]:
            from_city, to_city = city[0], city[1]
        else:
            from_city, to_city = city[1], city[0]
    if n > 2:
        print 'warning: more than 2 different cities found, I will take only the two first that appeared and put a *'
        srt = zip(loc,city)
        srt.sort() # taking the two first in order of appearance
        if srt[0][0] < srt[1][0]:
            from_city, to_city = [srt[0][1] + '*', srt[1][1] + '*']
        else:
            from_city, to_city = [srt[1][1] + '*', srt[0][1] + '*']
    return from_city, to_city

db = ["offering: SD (or anywhere along the way) to SLO tomorrow, Monday 5/30 leaving 7-8am $20", "Offering Sac --> SLO Sun 5/29 5pm Bay --> SLO Sun 5/29 7pm Im taking 880 to 101, so if anyone along the way needs a ride lmk. Bring gas $", "Seeking: SLO -> San Jose Friday 6/3 early afternoon", "Offering: SLO to SD, tomorrow (Friday) around noon", "Offering San Diego to Slo leaving around 12!", "SEEKING: OC/LA to SLO Sunday at any time 5/30 Willing to provide gas money Just need enough space in the ride for a small duffel bag and a normal sized backpack Hit me up if you're leaving tomorrow from anywhere in the OC/LA area! I can get a ride to where you leave. Thanks in advanced", "SEEEKING  SLO---> Sacramento area (El Dorado Hills) 6/11 or 6/12 I will be packed very lightly if space is an issue!", "Offering: LA (626 area) --> SLO Sunday night (5/29) around 9PM", "OFFERING SJ---->SLO Monday 5/30 Tomorrow @5pm", "OFFERING: San Jose -> SLO Tomorrow 5/30 around 11am -12","Offering: East bay (Union City) to sloMonday 6 PM 20$ :)","Offering: ride from East Bay (Concord/Walnut Creek) to SLOGas $:10$Leaving: 9 am Monday morning Comment below if interested","Offering:SF (Fisherman's Wharf area)--> SLO Tuesday 05/31 10am","OFFERING: SAC to SLOMonday 5/30 @4pBring $$$","Offering: Sac to SLO, taking the 5 Monday 5/30, not sure what time 2 spots $","OFFERING: Roseville/Sacramento --> SLO Monday May 30th @ 11am $20 for gas please!","SEEKING from SLO to SF tomorrow night pitch for gas", "Offering: San Diego to SLO Date: Saturday, 5/28 around 1 PM My sister is driving up for memorial day so if you have friends or family coming up who need a ride message me! She's asking $20", "SEEKING:SF (or any Bart station) to SLO monday 5/30 afternoon petrol $$$ is a given!", "Last minute offering! SLO to Davis/Sacramento tomorrow morning (5/28) at 7 am!"]

# building keywords for each city and a dictionary
 # dictionary of possible cities and their keywords

post_type = list()
from_city = list()
to_city = list()
date = list()
period = list()
hour = list()

for post in db:
    post_type.append(get_type(post))
    orig, dest = get_route(post)
    from_city.append(orig)
    to_city.append(dest)

out = zip(post_type,from_city,to_city, db)
	
