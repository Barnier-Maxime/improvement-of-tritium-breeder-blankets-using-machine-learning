import openmc
import os
import json
import numpy as np
from numpy import random
import re 
import random
from tqdm import tqdm
import matplotlib.pyplot as plt
from uncertainties import unumpy
from material_maker_functions import *

def make_breeder_material(enrichment_fraction, breeder_material_name, temperature_in_C,id): #give the chemical expression for the name
    print('enrichment_fraction',enrichment_fraction)
    if enrichment_fraction > 1.0:
        enrichment_fraction = 1.0
        print('enrichment can not be higher than 1.0')
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
def make_materials_geometry_tallies(enrichment_fractions, breeder_material_name, temperature_in_C, batches, nps, include_first_wall,seed): #thickness fixed to 100cm and inner radius to 500cm
    os.system('rm *.h5')
    os.system('rm *.xml')
    print('simulating ',' batches =',batches,'seed = ',seed, 'nps', nps, 'enrichment_fractions', enrichment_fractions,'inner radius = 500','thickness = 100 breeder_material_name =',breeder_material_name)
 
    number_of_materials=len(enrichment_fractions)

    print(enrichment_fractions)

    #MATERIALS#

    list_of_breeder_materials =[]

    for counter, e in enumerate(enrichment_fractions):
        breeder_material = make_breeder_material(e,breeder_material_name,temperature_in_C,counter+3)
        list_of_breeder_materials.append(breeder_material)

    print('len(list_of_breeder_materials)',len(list_of_breeder_materials))
    mats = openmc.Materials(list_of_breeder_materials)
    eurofer = make_eurofer()
    mats.append(eurofer)
    mats.export_to_xml()

    # #GEOMETRY#
    list_of_breeder_blanket_region = []
    list_of_breeder_blanket_cell = []
        
    if include_first_wall == True:
        breeder_blanket_inner_surface_wall = openmc.Sphere(r=498) #inner radius
        first_wall_outer_surface = openmc.Sphere(r=500)
            
        inner_void_region_wall = -breeder_blanket_inner_surface_wall #inner radius
        inner_void_cell_wall = openmc.Cell(region=inner_void_region_wall) 
        inner_void_cell_wall.name = 'inner_void'

        first_wall_region = -first_wall_outer_surface & +breeder_blanket_inner_surface_wall
        first_wall_cell = openmc.Cell(region=first_wall_region)
        first_wall_cell.name = 'first_wall'
        first_wall_cell.fill = eurofer
        for k in range(1,number_of_materials+1):
            if k==number_of_materials:
                breeder_blanket_outer_surface= openmc.Sphere(r=500+100,boundary_type='vacuum')
            else:
                breeder_blanket_outer_surface = openmc.Sphere(r=500+k*(100/number_of_materials)) #inner radius + thickness of each breeder material
                
            list_of_breeder_blanket_region.append(-breeder_blanket_outer_surface & +first_wall_outer_surface)

            breeder_cell = openmc.Cell(region=-breeder_blanket_outer_surface & +first_wall_outer_surface)
            breeder_cell.fill = list_of_breeder_materials[k-1]
            breeder_cell.name = 'breeder_blanket' 

            list_of_breeder_blanket_cell.append(breeder_cell)

            if k!=number_of_materials:
                first_wall_outer_surface = breeder_blanket_outer_surface
 
        cells = [inner_void_cell_wall, first_wall_cell] + list_of_breeder_blanket_cell

    else:
        breeder_blanket_inner_surface_no_wall = openmc.Sphere(r=500) #inner radius
            
        inner_void_region_no_wall = -breeder_blanket_inner_surface_no_wall #inner radius
        inner_void_cell_no_wall = openmc.Cell(region=inner_void_region_no_wall) 
        inner_void_cell_no_wall.name = 'inner_void'

        for k in range(1,number_of_materials+1):
                if k==number_of_materials:
                    breeder_blanket_outer_surface= openmc.Sphere(r=500+100,boundary_type='vacuum')
                else:
                    breeder_blanket_outer_surface = openmc.Sphere(r=500+k*(100/number_of_materials)) #inner radius + thickness of each breeder material
                
                list_of_breeder_blanket_region.append(-breeder_blanket_outer_surface & +breeder_blanket_inner_surface_no_wall)

                breeder_cell = openmc.Cell(region=-breeder_blanket_outer_surface & +breeder_blanket_inner_surface_no_wall)
                breeder_cell.fill = list_of_breeder_materials[k-1]
                breeder_cell.name = 'breeder_blanket' 

                list_of_breeder_blanket_cell.append(breeder_cell)

                if k!=number_of_materials:
                    breeder_blanket_inner_surface_common = breeder_blanket_outer_surface
                cells = [inner_void_cell_no_wall] + list_of_breeder_blanket_cell

    universe = openmc.Universe(cells = cells)                       

    geom = openmc.Geometry(universe)

    #openmc color by material

    geom.export_to_xml()
    # p = openmc.Plot()
    # p.basis='xz'
    # p.filename = 'plot'
    # p.width = (1850, 1850) #hint, this might need to be increased to see the new large geometry
    # p.pixels = (1400, 1400) 
    # p.color_by = 'material'
    # #p.colors = {natural_lead: 'blue'}
    # plots = openmc.Plots([p])
    # plots.export_to_xml()

    # openmc.plot_geometry()

    # os.system('convert plot.ppm plot.png')
    # os.system('eog plot.png')
    # os.system('xdg-open plot.png')

    #SIMULATION SETTINGS#

    sett = openmc.Settings()
    sett.batches = batches
    sett.inactive = 0
    sett.particles = nps
    sett.seed = seed
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

    var=0
    df =tally.get_pandas_dataframe()     
    for sigma in df['std. dev.']:
        var+=sigma**2 #independance which is considered between the different layers
    tally_std_dev=(var)**(1/2)

    if len(set(enrichment_fractions)) == 1:
        graded = 'uniform'
    else:
        graded= 'graded'

    json_output= {'first_wall':include_first_wall,
                  'number_of_materials':len(enrichment_fractions),
                  'graded':graded,
                  'enrichment_value':enrichment_fractions,
                  'value': tally_result,
                  'std_dev': tally_std_dev,
                  'breeder_material_name':breeder_material_name,
                  'nps':nps
                  }

    print(json_output)
    return json_output
   
def find_tbr_dict(enrichment_fractions_simulation, breeder_material_name, include_first_wall, nps):
    result = make_materials_geometry_tallies(enrichment_fractions=enrichment_fractions_simulation,
                                            breeder_material_name = breeder_material_name, 
                                            temperature_in_C=500,
                                            batches=4,
                                            nps=nps,
                                            include_first_wall=include_first_wall,
                                            seed=1
                                            )
    return result


def find_tbr(enrichment_fractions_simulation, seed):

    result = make_materials_geometry_tallies(enrichment_fractions=enrichment_fractions_simulation,
                                            breeder_material_name = 'Li', 
                                            temperature_in_C=500,
                                            batches=4,
                                            nps=int(10000),
                                            include_first_wall=False ,
                                            seed=seed
                                            )
    return 1/result['value']
