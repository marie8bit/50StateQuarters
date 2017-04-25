import requests
import json
import os
stateImage = 'stateImage'

states_abbr = json.load(open('us_states_abbr.json.txt'))
print (states_abbr)
for key in states_abbr:

    abr = states_abbr[key]
    print (abr)
    url = 'https://www.usmint.gov/images/mint_programs/50sq_program/states/'+abr+'_Designs.gif'
    print(url)
    imageResponse = requests.get(url, stream = True)
    filename ='{}.gif'.format(abr)
    filepath = os.path.join(stateImage, filename)
    with open(filepath, 'wb') as file:

        for chunk in imageResponse.iter_content(chunk_size=128):
            file.write(chunk)
