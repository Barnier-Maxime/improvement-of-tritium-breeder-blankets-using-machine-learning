from geometry_breeder_material import *
import argparse 



def simulate(nps =1000, num_simulations=3,number_of_materials = 2,num_uniform_simulations=2, include_first_wall=True,outputfile='results/simulation_results_2_layers_random_first_wall.json'):
    breeder_material_names=['Li','Li4SiO4','Li2TiO3']
    results = []

    if num_uniform_simulations != 0:
        for i in tqdm(range(0,num_uniform_simulations+1)):

                enrichment_fractions_simulation = []
                breeder_material_name = random.choice(breeder_material_names)
                
                for j in range(0,number_of_materials):
                    enrichment_fractions_simulation.append((1.0/num_uniform_simulations)*i)

                inner_radius = 500
                thickness = 100

                result = find_tbr_dict(enrichment_fractions_simulation, breeder_material_name, include_first_wall, nps)
                results.append(result)


        print('finished uniform blanket simulations')


    for i in tqdm(range(0,num_simulations)):
            os.system('rm *.h5')
            enrichment_fractions_simulation = []
            breeder_material_name = random.choice(breeder_material_names)

            for j in range(0,number_of_materials):
                enrichment_fractions_simulation.append(random.uniform(0,1))

            inner_radius = 500
            thickness = 100
        
            result = find_tbr_dict(enrichment_fractions_simulation, breeder_material_name, include_first_wall, nps)
            results.append(result)


    with open(outputfile, 'w') as file_object:
        json.dump(results, file_object, indent=2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-nps', '--number_of_particles', default=100000)
    parser.add_argument('-num_sim', '--num_simulations', default=10000) 
    parser.add_argument('-num_mat', '--number_of_materials', default=2)    
    parser.add_argument('-num_uni_sim', '--num_uniform_simulations', default=1)    
    parser.add_argument('-first_wall', '--include_first_wall', default=True)    

    args = parser.parse_args()
    print('nps',type(args.number_of_particles),
             'num_simulations',args.num_simulations,
             'number_of_materials',args.number_of_materials,
             'num_uniform_simulations',args.num_uniform_simulations,
             'include_first_wall',args.include_first_wall)

    
    simulate(nps=int(args.number_of_particles),
             num_simulations=int(args.num_simulations),
             number_of_materials=int(args.number_of_materials),
             num_uniform_simulations=int(args.num_uniform_simulations),
             include_first_wall=bool(args.include_first_wall)        )
