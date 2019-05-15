# Machine_learning_project

This software is meant to test different materials for the tritium breeder blankets in Tokamak power plants and find the right one in each location.

Materials available include:
- Neutron multiplier
- Tritium breeder
- Neutron moderator

As Jonathan Shimwell shown it in an article named 'Fusion Engineering and Design', the beryllium is a really interesting material for fusion nuclear devices because it is a neutron multiplier and the Be(n,2n) reaction is endothermic (Q<0). The tritium breeder material is composed of lithium compound  : the reaction Li(n,t) is exothermic : it produces energy (most particularly heat). 

Two approaches are possible for the constitution of the blankets : the first one is a uniform multiplier fraction and the second is to put a variable fraction of multiplier (linear variation in first approach for example).  

The neutron multiplier front fraction must be higher than the rear fraction because as the reaction Be(n,2n) is endothermic, the peak heat is not very high in front of the blanket.

The use of non uniform neutron multiplier is very relevant because it is possible to reduce the mass of Be used to make the blanket without any bad effect on the peak heat or the energy multiplication. 

Basically, the project consists in modeling a blanket with a set of small cubes. On each cube, the program will have to find the optimal fraction of neutron multiplier and tritium breeder. 

As there are many different combinations, machine learning is really usefull and save a lot of time.