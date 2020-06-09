# AV.by Parser.


Script parses advertisemnts about cars for sale from https://av.by/ and saves in postgresql:
 
 
Script saves advertisemnts in database House_advertisements in table houses.


# Database structure:

# Table mark
	Column id is column for number of record.(autoadd)
	Column mark is column for mark of car.(Type is String)
	Column link is column for link to  car models.(Type is Sring)
 
# Table models
	Column id is column for number of record.(autoadd)
	Column model is column for model of car.(Type is String)
	Column link is column for link to  current car advertisements.(Type is Sring)
	Column mark_id is column for id of car mark.(Foreingkey is mark.id)
 
# Table car
	Column id is column for number of record.(autoadd)
	Column mark_id is column for id of car mark.(Foreingkey is mark.id)
	Column model_id is column for id of car model.(Foreingkey is mark.id)
	Column year is column foк year of manufacture of a car.(Type is String)
	Column link is column for link to car advertisement.(Type is Sring)
	Column cost is column for cost of car(Type is String).
	Column location is column for car location(Type is String)
 
	



