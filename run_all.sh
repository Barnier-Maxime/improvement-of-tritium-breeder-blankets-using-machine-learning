
# run this file with the following command in the terminal
# bash run_all.sh

python3 max_tbr_finder_halton.py


python3 max_tbr_finder_halton.py -nps 10000 --num_simulations 1000 -num_mat 2 -num_uni_sim 0 -first_wall True -o 'results/simulation_results_2_layers_halton_first_wall.json'

python3 max_tbr_finder_halton.py -nps 50000 --num_simulations 5000 -num_mat 3 -num_uni_sim 0 -first_wall True -o 'results/simulation_results_3_layers_halton_first_wall.json'

python3 max_tbr_finder_halton.py -nps 100000 --num_simulations 10000 -num_mat 4 -num_uni_sim 0 -first_wall True -o 'results/simulation_results_4_layers_halton_first_wall.json'
