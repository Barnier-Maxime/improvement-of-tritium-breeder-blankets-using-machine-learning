import openmc
import os
import json
import numpy as np
from numpy import random
import re 
from tqdm import tqdm
import matplotlib.pyplot as plt

from material_maker_functions import *

def make_breeder_material(enrichment_fraction, breeder_material_name, temperature_in_C,id): #give the chemical expression for the name

    #density data from http://aries.ucsd.edu/LIB/PROPS/PANOS/matintro.html

    natural_breeder_material = openmc.Material(2, "natural_breeder_material")
    breeder_material = openmc.Material(id, breeder_material_name) # this is for enrichmed Li6 

    element_numbers = get_element_numbers(breeder_material_name)
    elements = get_elements(breeder_material_name)

    for e, en in zip(elements, element_numbers):
        natural_breeder_material.add_element(e, en,'ao')

    for e, en in zip(elements, element_numbers):
        if e == 'Li':
            breeder_material.add_nuclide('Li6', en * enrichment_fraction, 'ao')
            breeder_material.add_nuclide('Li7', en * (1.0-enrichment_fraction), 'ao')  
        else:
            breeder_material.add_element(e, en,'ao')    

    density_of_natural_material_at_temperature = find_density_of_natural_material_at_temperature(breeder_material_name,temperature_in_C,natural_breeder_material)

    natural_breeder_material.set_density('g/cm3', density_of_natural_material_at_temperature)
    atom_densities_dict = natural_breeder_material.get_nuclide_atom_densities()
    atoms_per_barn_cm = sum([i[1] for i in atom_densities_dict.values()])

    breeder_material.set_density('atom/b-cm',atoms_per_barn_cm) 

    return breeder_material

def make_materials_geometry_tallies(batches,enrichment_fractions,breeder_material_name,temperature_in_C): #thickness fixed to 100cm and inner radius to 500cm
    print('simulating ',batches,enrichment_fractions,'inner radius = 500','thickness = 100',breeder_material_name)

    number_of_materials=len(enrichment_fractions)

    print(enrichment_fractions)

    #MATERIALS#

    list_of_breeder_materials =[]

    for counter, e in enumerate(enrichment_fractions):
        breeder_material = make_breeder_material(e,breeder_material_name,temperature_in_C,counter+3)
        list_of_breeder_materials.append(breeder_material)

    print('len(list_of_breeder_materials)',len(list_of_breeder_materials))
    mats = openmc.Materials(list_of_breeder_materials)
    mats.export_to_xml()

    # #GEOMETRY#

    breeder_blanket_inner_surface = openmc.Sphere(r=500) #inner radius
    inner_void_region = -breeder_blanket_inner_surface #inner radius
    inner_void_cell = openmc.Cell(region=inner_void_region) 
    inner_void_cell.name = 'inner_void'
    
    
    list_of_breeder_blanket_region = []
    list_of_breeder_blanket_cell = []
    

    for k in range(1,number_of_materials+1):

        if k==number_of_materials:
            breeder_blanket_outer_surface= openmc.Sphere(r=500+100,boundary_type='vacuum')
        else:
            breeder_blanket_outer_surface = openmc.Sphere(r=500+k*(100/number_of_materials)) #inner radius + thickness of each breeder material
        
        list_of_breeder_blanket_region.append(-breeder_blanket_outer_surface & +breeder_blanket_inner_surface)

        breeder_cell = openmc.Cell(region=-breeder_blanket_outer_surface & +breeder_blanket_inner_surface)
        breeder_cell.fill = list_of_breeder_materials[k-1]
        breeder_cell.name = 'breeder_blanket' 

        list_of_breeder_blanket_cell.append(breeder_cell)

        if k!=number_of_materials:
            breeder_blanket_inner_surface = breeder_blanket_outer_surface
   
 
    cells = [inner_void_cell] + list_of_breeder_blanket_cell

    universe = openmc.Universe(cells = cells)                              

    geom = openmc.Geometry(universe)

    #openmc color by material

    #plt.show(universe.plot(width=(2000,2000),basis='xz',colors={inner_void_cell: 'blue',list_of_breeder_blanket_cell[0] : 'yellow',list_of_breeder_blanket_cell[1] : 'green', list_of_breeder_blanket_cell[2]: 'red'}))
    geom.export_to_xml()


    #SIMULATION SETTINGS#

    sett = openmc.Settings()
    sett.batches = batches
    sett.inactive = 0
    sett.particles = 5000
    sett.run_mode = 'fixed source'

    source = openmc.Source()
    source.space = openmc.stats.Point((0,0,0))
    source.angle = openmc.stats.Isotropic()
    source.energy = openmc.stats.Muir(e0=14080000.0, m_rat=5.0, kt=20000.0) #neutron energy = 14.08MeV, AMU for D + T = 5, temperature is 20KeV
    sett.source = source

    #TALLIES#

    tallies = openmc.Tallies()
    cell_filter_breeder = openmc.CellFilter(list_of_breeder_blanket_cell)

    tally = openmc.Tally(name='TBR')  
    tally.filters = [cell_filter_breeder]
    tally.scores = ['205']
    tallies.append(tally)


    #RUN OPENMC #

    model = openmc.model.Model(geom, mats, sett, tallies)
    model.run()

    sp = openmc.StatePoint('statepoint.'+str(batches)+'.h5')

    tally = sp.get_tally(name='TBR')


    tally_result = tally.get_values().sum() 

    # df =tally.get_pandas_dataframe()  
    # tally_result = df['mean'].sum() 

    json_output= {'enrichment_value':enrichment_fractions,
                            'value': tally_result,
                                # 'std_dev': tally_std_dev
                                }

    print(json_output)
    return json_output
   
os.system('rm *.h5')

num_simulations=20000
number_of_materials = 3
num_uniform_simulations=100

# results_uniform = []
# for i in tqdm(range(0,num_uniform_simulations+1)):
#         os.system('rm *.h5')
#         enrichment_fractions_simulation = []
#         breeder_material_name = 'Li'
        
#         for j in range(0,number_of_materials):
#             enrichment_fractions_simulation.append((1.0/num_uniform_simulations)*i)

#         inner_radius = 500
#         thickness = 100

#         result = make_materials_geometry_tallies(batches=4,
#                                                 enrichment_fractions=enrichment_fractions_simulation,
#                                                 breeder_material_name = breeder_material_name, 
#                                                 temperature_in_C=500
#                                                 )
#         results_uniform.append(result)


# with open('simulation_results_'+str(number_of_materials)+'_layers_uni_100.json', 'w') as file_object:
#     json.dump(results_uniform, file_object, indent=2)



results = []
for i in tqdm(range(0,num_simulations)):
        os.system('rm *.h5')
        enrichment_fractions_simulation = []
        breeder_material_name = 'Li'
        
        for j in range(0,number_of_materials):
            enrichment_fractions_simulation.append(random.uniform(0, 1))

        inner_radius = 500
        thickness = 100

        result = make_materials_geometry_tallies(batches=4,
                                                enrichment_fractions=enrichment_fractions_simulation,
                                                breeder_material_name = breeder_material_name, 
                                                temperature_in_C=500
                                                )
        results.append(result)


with open('simulation_results_'+str(number_of_materials)+'_layers_non_uni_20000.json', 'w') as file_object:
    json.dump(results, file_object, indent=2)