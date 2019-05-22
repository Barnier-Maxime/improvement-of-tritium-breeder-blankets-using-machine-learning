import openmc
import os
import json
import numpy as np
from numpy import random
import re 
from tqdm import tqdm

from material_maker_functions import *

def make_breeder_material(enrichment_fraction, breeder_material_name, temperature_in_C): #give the chemical expression for the name

    #density data from http://aries.ucsd.edu/LIB/PROPS/PANOS/matintro.html

    natural_breeder_material = openmc.Material(2, "natural_breeder_material")
    breeder_material = openmc.Material(1, breeder_material_name) # this is for enrichmed Li6 

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
    print('simulating ',batches,enrichment_fraction,'inner radius = 500','thickness = 100',breeder_material_name)

    number_of_materials=len(enrichment_fractions)

    #MATERIALS#

    list_of_breeder_materials =[]

    for e in enrichment_fractions:
        breeder_material = make_breeder_material(e,breeder_material_name,temperature_in_C)
        list_of_breeder_materials.append(breeder_material)

    eurofer = make_eurofer()

    mats = openmc.Materials(list_of_breeder_materials+[eurofer])


    #GEOMETRY#

    breeder_blanket_inner_surface = openmc.Sphere(R=500) #inner radius
    list_of_breeder_blanket_region = []
    list_of_breeder_blanket_cell = []
    

    for k in range (1,number_of_materials+1):
        breeder_blanket_outer_surface = openmc.Sphere(R=500+k*(100/number_of_materials)) #inner radius + thickness of each breeder material
        list_of_breeder_blanket_region.append (-breeder_blanket_outer_surface & +breeder_blanket_inner_surface)
        list_of_breeder_blanket_cell.append (openmc.Cell(region=-breeder_blanket_outer_surface & +breeder_blanket_inner_surface))
        openmc.Cell(region=-breeder_blanket_outer_surface & +breeder_blanket_inner_surface).fill = list_of_breeder_materials[k-1]
        openmc.Cell(region=-breeder_blanket_outer_surface & +breeder_blanket_inner_surface).name = 'breeder_blanket' 
        breeder_blanket_inner_surface = breeder_blanket_outer_surface
   

    vessel_inner_surface = openmc.Sphere(R=500+100+10) #inner radius + thickness + 10
    vessel_outer_surface = openmc.Sphere(R=500+100+20,boundary_type='vacuum') #inner radius + thickness + 20

    #breeder_blanket_region = -breeder_blanket_outer_surface & +breeder_blanket_inner_surface
    #breeder_blanket_cell = openmc.Cell(region=breeder_blanket_region) 
    #breeder_blanket_cell.fill = breeder_material
    #breeder_blanket_cell.name = 'breeder_blanket'

    inner_void_region = -openmc.Sphere(R=500) #inner radius
    inner_void_cell = openmc.Cell(region=inner_void_region) 
    inner_void_cell.name = 'inner_void'

    vessel_region = +vessel_inner_surface & -vessel_outer_surface
    vessel_cell = openmc.Cell(region=vessel_region) 
    vessel_cell.name = 'vessel'
    vessel_cell.fill = eurofer

    blanket_vessel_gap_region = -vessel_inner_surface & +openmc.Sphere(R=500+100)
    blanket_vessel_gap_cell = openmc.Cell(region=blanket_vessel_gap_region) 
    blanket_vessel_gap_cell.name = 'blanket_vessel_gap'    

    universe = openmc.Universe(cells=[inner_void_cell, 
                                      list_of_breeder_blanket_cell,
                                      blanket_vessel_gap_cell,
                                      vessel_cell])

    geom = openmc.Geometry(universe)

    #SIMULATION SETTINGS#

    sett = openmc.Settings()
    #batches = 3 # this is parsed as an argument
    sett.batches = batches
    sett.inactive = 10
    sett.particles = 500
    sett.run_mode = 'fixed source'

    source = openmc.Source()
    source.space = openmc.stats.Point((0,0,0))
    source.angle = openmc.stats.Isotropic()
    source.energy = openmc.stats.Muir(e0=14080000.0, m_rat=5.0, kt=20000.0) #neutron energy = 14.08MeV, AMU for D + T = 5, temperature is 20KeV
    sett.source = source

    #TALLIES#

    tallies = openmc.Tallies()

    # define filters
    list_of_cell_filter_breeder = []
    list_of_particle_filter = []

    #cell_filter_breeder = openmc.CellFilter(breeder_blanket_cell)

    for l in range (number_of_materials):
        list_of_cell_filter_breeder.append(openmc.CellFilter(list_of_breeder_blanket_cell[l]))
        list_of_particle_filter.append(openmc.ParticleFilter([1])) #1 is neutron, 2 is photon

    #particle_filter = openmc.ParticleFilter([1]) #1 is neutron, 2 is photon

    
    #tally = openmc.Tally(name='TBR')
    #tally.filters = [cell_filter_breeder, particle_filter]
    #tally.scores = ['205']
    #tallies.append(tally)

    for u in range (number_of_materials):
        tally = openmc.Tally(name='TBR')
        tally.filters = [list_of_cell_filter_breeder[u],list_of_particle_filter[u] ]
        tally.scores = ['205']
        tallies.append(tally)  


    #RUN OPENMC #

    model = openmc.model.Model(geom, mats, sett, tallies)
    model.run()

    sp = openmc.StatePoint('statepoint.'+str(batches)+'.h5')

    json_output = {'enrichment_fraction': enrichment_fractions,
                   'inner_radius': 500,
                   'thickness': 100,
                   'breeder_material_name': breeder_material_name,
                   'temperature_in_C': temperature_in_C}

    tallies_to_retrieve = ['TBR', 'DPA', 'blanket_leakage', 'vessel_leakage']
    for tally_name in tallies_to_retrieve:
        tally = sp.get_tally(name=tally_name)
        # for some reason the tally sum is a nested list
        tally_result = tally.sum[0][0][0]/batches
        # for some reason the tally std_dev is a nested list
        tally_std_dev = tally.std_dev[0][0][0]/batches

        json_output[tally_name] = {'value': tally_result,
                                   'std_dev': tally_std_dev}

    spectra_tallies_to_retrieve = ['breeder_blanket_spectra', 'vacuum_vessel_spectra']
    for spectra_name in spectra_tallies_to_retrieve:
        spectra_tally = sp.get_tally(name=spectra_name)
        spectra_tally_result = [entry[0][0] for entry in spectra_tally.mean]
        spectra_tally_std_dev = [entry[0][0]
                                 for entry in spectra_tally.std_dev]

        json_output[spectra_name] = {'value': spectra_tally_result,
                                     'std_dev': spectra_tally_std_dev,
                                     'energy_groups': list(energy_bins)}


    return json_output
   
results = []
num_simulations=10
number_of_materials = 3

for i in tqdm(range(0,num_simulations)):
        breeder_material_name = 'Li'

        for j in range(0,number_of_materials):
            enrichment_fraction = (j+1)*1/number_of_materials
            enrichment_fractions.append(enrichment_fraction)

        inner_radius = 500
        thickness = 100

        result = make_materials_geometry_tallies(batches=4,
                                                enrichment_fraction=enrichment_fractions,
                                                breeder_material_name = breeder_material_name, 
                                                temperature_in_C=500
                                                )
        results.append(result)


with open('simulation_results.json', 'w') as file_object:
    json.dump(results, file_object, indent=2)