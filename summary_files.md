# Summary of the different programs and files inside the git repository

This text file is meant to explain the utility of the different programs and files on the git repository of the project.

- Python files (programs)

cube_viewer.py : construction of cubes and visualization (useful for the improvement of the project in order to make angular layers)

convert_df_tf.py / convert_df_tf_git.py / convert_df_tf_test.py : converts a pandas dataframe into a tensorflow dataset (useful to use keras and to create data for neural networks)

max_tbr_finder.py / max_tbr_finder_halton.py / max_tbr_finder_random.py : create the dataset containing the simulation results of OpenMC. The selection method of the enrichment fractions of the different layers can be random, based on a halton sequence. These programs return the dataset.

max_tbr_finder_scipy.py / max_tbr_finder_noisyopt.py : optimization of the max tbr using scipy.minimoze or noisyopt.

correlation_study.py / correlation_study_halton_sample.py / correlation_study_random_sample.py : uses the dataset created with the previous prgrams and return a correlation study plot between the enrichment fraction in Li6 of each layer and the TBR values.

material_maker_functions.py : create the different breeder materials for the study

geometry_breeder_material.py : main program for the simulations. Uses OpenMC to create the geometry of the tokamak, the tallies, the neutron source, the materials and the settings of the simulations.

json_file_plot_results.py / json_plot_results_noisyopt_updatemenus.py : plot the results of TBR as a function of the enrichment fraction of each layer for a 3 layers model (3D plot : each axis is an enrichment fraction) the color of the simulation point is a function of the intensity of the TBR (colorscale).

enrichment_with_radius_layer.py : plots the enrichment fraction in Li6 as a function of the radius in the breeder blanket for the best TBR.

prediction_function.py : creation of a keras model for the neural network and prediction of the TBR using a dataset containing a list of TBR and enrichment fraction values as input.

gaussian_process_regression.py / gaussian_process_regression_2_4_layers.py : optimization program. Removes the worst TBR point and add a new simulation point close to the best TBR value : the dataset is modified several times and the plot of the results is improved.

gaussian_process_inference.py / gaussian_process_inference_2_4_layers.py : makes a gaussian regression with the dataset and removes the lowest TBr point and add a new one at the max predicted value for the TBR.

- Results files :

json_files_point_source : contains several json files for the simulations of the TBR with uniform and non uniform materials with a number of layers between 1 and 7.

results_point_source : simulation results with several materials with and wothout the first wall.

parametric_plasma_source : parametric plasma source creation programs.

results_new_source : contains all the simulation results for the use of machine learning (keras, neural networks, gaussian process...) using the parametric neutron source : computing time in quite long because of the source.

- Plots :

plots_point_source :  plots of TBR as a function of the number of layers for several materials with noisyopt.

plots_new_neutron_source : plots of the TBR as a function of the enrichment fractions of each layer for a 3 layers model using gaussian process regression.

- Bash file :

run_all.sh : bash file for simulating everything in one time.

- Dockerfile :

Dockerfile : docker image to build on a new computer and the to run in order to have access to python3, OpenMC tools...










