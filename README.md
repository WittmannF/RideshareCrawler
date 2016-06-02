# RideshareCrawler
This code tries to understand routes, dates and types of offers from posts of rideshare foruns. For example the following post:

  "Offering:
  SLO to San Diego 
  Tomorrow Thursday 5/26 leaving around 6 or 7pm
  Requesting $20 for gas
  Message me if you need a ride!"

Will return the following information:
  post_type = 'offering'
  from_city = 'sd'
  to_city = 'slo'

The ultimate goal is to serve as backend tool to identify any kind of post from rideshare foruns. The next steps in the given code are to find bugs, to consider posts when someone post a trip back and to understand the dates. 
