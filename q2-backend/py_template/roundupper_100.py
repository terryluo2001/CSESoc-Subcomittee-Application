from dataclasses import dataclass
from enum import Enum
from typing import Union, NamedTuple, List
from flask import Flask, request
import math

# SpaceCowboy models a cowboy in our super amazing system
@dataclass
class SpaceCowboy:
    name: str
    lassoLength: int

# SpaceAnimal models a single animal in our amazing system
@dataclass
class SpaceAnimal:
    # SpaceAnimalType is an enum of all possible space animals we may encounter
    class SpaceAnimalType(Enum):
        PIG = "pig"
        COW = "cow"
        FLYING_BURGER = "flying_burger"

    type: SpaceAnimalType

# SpaceEntity models an entity in the super amazing (ROUND UPPER 100) system
@dataclass
class SpaceEntity:
    class Location(NamedTuple):
        x: int
        y: int

    metadata: Union[SpaceCowboy, SpaceAnimal]
    location: Location

# ==== HTTP Endpoint Stubs ====
app = Flask(__name__)
space_database: List[SpaceEntity] = []

# the POST /entity endpoint adds an entity to your global space database
@app.route('/entity', methods=['POST'])
def create_entity():
    # TODO: implement me
    data = request.get_json()

    #If the request body is valid
    if data is not None: 
        if "entities" in data:
            entities = data.get("entities")

            #Loop through each supposed entity
            for entity in entities:   
                space_database.append(entity)
            
        #If the request body isn't empty, but the format is not correct
        else:
            return {}, 400

    #If request body is empty
    else: 
        return {}, 400
        
    #Return HTTP 200
    return {}, 200

# lasooable returns all the space animals a space cowboy can lasso given their name
@app.route('/lassoable', methods=['GET'])
def lassoable():
    # TODO: implement me
    data = request.get_json()

    #The space cowboy matching
    space_cowboy = {}

    #A list showing all the space animals in the database
    original_space_animals = []

    #If the data is not empty
    if data is not None:

        #If the syntax is correct
        if "cowboy_name" in data:
            cowboy_name = data.get("cowboy_name")

            #Finding the space cowboy with matching name and all the space animals
            for entity in space_database:
                if entity.get("type") == "space_cowboy" and entity.get("metadata").get("name") == cowboy_name:
                    space_cowboy = entity
                elif entity.get("type") == "space_animal":
                    original_space_animals.append(entity)
            
            #A list of all the lassoable space animals
            final_space_animals = []
            for space_animal in original_space_animals:

                #Have to make sure a matching cowboy is found
                if len(space_cowboy) != 0:

                    #Distance formula
                    if math.sqrt((space_animal.get("location").get("x")-space_cowboy.get("location").get("x"))**2+(space_animal.get("location").get("y")-space_cowboy.get("location").get("y"))**2) <= space_cowboy.get("metadata").get("lassoLength"):

                        #Append the space animal to returned statement
                        final_space_animals.append({"type": space_animal.get("metadata").get("type"), "location": space_animal.get("location")})
                    
            return {"space_animals": final_space_animals}, 200
        
        #If the syntax isn't correct
        else:
            return {}, 400

    #If the data is empty
    else:
        return {}, 400

#Handling code 404
@app.errorhandler(404)
def invalid_route(e):
    return "Invalid route"

# DO NOT TOUCH ME, thanks :D
if __name__ == '__main__':
    app.run(debug=True, port=8080)