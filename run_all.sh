
# run this file with the following command in the terminal
# bash run_all.sh

python3 max_tbr_finder_halton.py


python3 max_tbr_finder_halton.py -nps 100000 --num_simulations 200 -num_mat 2 -num_uni_sim 0 -first_wall True -o 'results_new_neutron_source/simulation_results_2_layers_halton_first_wall_neural_network.json'

python3 max_tbr_finder_halton.py -nps 500000 --num_simulations 500 -num_mat 3 -num_uni_sim 0 -first_wall True -o 'results_new_neutron_source/simulation_results_3_layers_halton_first_wall_neural_network.json'

python3 max_tbr_finder_halton.py -nps 1000000 --num_simulations 1000 -num_mat 4 -num_uni_sim 0 -first_wall True -o 'results_new_neutron_source/simulation_results_4_layers_halton_first_wall_neural_network.json'
