#need a Backus Naur form grammer to implement Genetic algorithm using pyneurgen
import xlrd
import math
import random
import pyneurgen
from pyneurgen.grammatical_evolution import GrammaticalEvolution
from pyneurgen.fitness import FitnessElites, FitnessTournament
from pyneurgen.fitness import ReplacementTournament, MAX, MIN, CENTER
from pyneurgen.neuralnet import NeuralNet
from pyneurgen.nodes import Node, BiasNode, CopyNode, Connection
from pyneurgen.layers import Layer
from pyneurgen.recurrent import JordanRecurrent
#i changed the max_epochs to get it run faster as a code confirmation
#now on training apply around 1000 epochs
bnf="""
<model_name>        ::= sample<member_no>.nn
<max_hnodes>        ::= 15
<node_type>         ::= sigmoid | linear | tanh
<positive-real>     ::= 2.<int-const>
<int-const>         ::= <int-const> | 1 | 2 | 3 | 4 | 5 | 6 |
                        7 | 8 | 9 | 0
<sign>              ::= + | -
<max_epochs>        ::= 1000 
<starting_weight>   ::= <sign> 0.<int-const> | <sign> 1.<int-const> |
                        <sign> 2.<int-const> | <sign> 3.<int-const> |
                        <sign> 4.<int-const> | <sign> 5.<int-const>
<learn_rate>        ::= 0.2<int-const>
<saved_name>        ::= hybrid

<S>		::=
import math
import random

from pyneurgen.neuralnet import NeuralNet
from pyneurgen.nodes import Node, BiasNode, CopyNode, Connection
from pyneurgen.layers import Layer
from pyneurgen.recurrent import JordanRecurrent

net = NeuralNet()
hidden_nodes = max(int(round(<positive-real> * float(<max_hnodes>))), 1)

net.init_layers(len(self.all_inputs[0]),
                [hidden_nodes],
                len(self.all_targets[0]))

net.layers[1].set_activation_type('<node_type>')
net.output_layer.set_activation_type('<node_type>')

#   Use the genotype to get starting weights
for layer in net.layers[1:]:
    for node in layer.nodes:
        for conn in node.input_connections:
            #   every time it is asked, another starting weight is given
            conn.set_weight(self.runtime_resolve('<starting_weight>', 'float'))

# Note the injection of data from the genotype
# In a real project, the genotype might pull the data from elsewhere.
net.set_all_inputs(self.all_inputs)
net.set_all_targets(self.all_targets)

length = len(self.all_inputs)
learn_end_point = int(length * .6)
validation_end_point = int(length * .8)

net.set_learn_range(0, learn_end_point)

net.set_validation_range(0, learn_end_point)
net.set_validation_range(learn_end_point + 1, validation_end_point)
net.set_test_range(validation_end_point + 1, length - 1)

net.set_learnrate(<learn_rate>)
epochs = int(round(<positive-real> * float(<max_epochs>)))

if epochs > 0:
    #   Use learning to further set the weights
    net.learn(epochs=epochs, show_epoch_results=True,
        random_testing=False)

#   Use validation for generating the fitness value
mse = net.validate(show_sample_interval=0)

print "mse", mse
modelname = self.runtime_resolve('<model_name>', 'str')

net.save(modelname)

self.set_bnf_variable('<saved_name>', modelname)

#   This method can be used to look at all the particulars
#       of what happened...uses disk space
self.net = net
fitness = mse
self.set_bnf_variable('<fitness>', fitness)

            """



ges = GrammaticalEvolution()

ges.set_bnf(bnf)
ges.set_genotype_length(start_gene_length=100,
                        max_gene_length=200)

ges.set_population_size(20)
ges.set_max_generations(1) #controls the maximum generations of the genes i changed here
ges.set_fitness_type('center', 0.01)

ges.set_max_program_length(4000)

ges.set_wrap(True)
ges.set_fitness_fail(2.0)
ges.set_mutation_type('m')
ges.set_max_fitness_rate(.25)
ges.set_mutation_rate(.025)
ges.set_fitness_selections(
    FitnessElites(ges.fitness_list, .05),
    FitnessTournament(ges.fitness_list, tournament_size=2))

ges.set_crossover_rate(.2)
ges.set_children_per_crossover(2)

ges.set_replacement_selections(
        ReplacementTournament(ges.fitness_list, tournament_size=3))

ges.set_maintain_history(True)
ges.set_timeouts(10, 360)
#   All the parameters have been set.

ges.create_genotypes()
"""
#   all samples are drawn from this population
pop_len = 20
factor = 1.0 / float(pop_len)
population = [[i, math.sin(float(i) * factor * 10.0) + \
                random.gauss(factor, .2)]
                    for i in range(pop_len)]
"""
all_inputs = []
all_targets = []
"""
def population_gen(population):
    
    This function shuffles the values of the population and yields the
    items in a random fashion.

    

    pop_sort = [item for item in population]
    random.shuffle(pop_sort)

    for item in pop_sort:
        yield item"""
# above function is not required as it generates sampled random data for testing purpose
# read the excel files to load the inputs
#   Build the inputs
workbook=xlrd.open_workbook('d_set_all_50_centerofmass.xls',on_demand= True)
worksheet=workbook.sheet_by_index(0)
#workbook.nsheets gives number of sheets and #workbook.sheet_names() gives the list of names present in the file

#sheet.cell(row,column) gives the value of the particular cell xlrd.empty_cell.value returns empty cell value
row=0
column=16
"""for position, target in population_gen(population):
    all_inputs.append([float(position) / float(pop_len), random.random()])
    all_targets.append([target])"""
print "opening the sheet to read values"
while row<300:
	inc=0
	temp=[] #empty list for each training example
	print "iterating through each row"
	while inc<14:
		#print worksheet.cell(row,column+inc).value
		temp.append(worksheet.cell(row,column+inc).value)
		inc+=1
	all_inputs.append(temp)
	row+=1

print all_inputs

#reading the label vector
row=301
column=16

while row<601:
	inc=0
	temp=[] #empty list for each training output
	print "iterating through each row"
	while inc<50:
		#print worksheet.cell(row,column+inc).value
		temp.append(worksheet.cell(row,column+inc).value)
		inc+=1
	all_targets.append(temp)
	row+=1
print all_targets

for g in ges.population:
	ges.all_inputs = all_inputs
	ges.all_targets = all_targets

#at first i didnt get how to stop that network :P
#i need to control the max_generations and fix the epochs 
#at this time 4 am i am not going to run the network dont know when it will converge
print ges.run()
print "Final Fitness list sorted best to worst:"
print ges.fitness_list.sorted()
print
print
g = ges.population[ges.fitness_list.best_member()]
program = g.local_bnf['program']

saved_model = g.local_bnf['<saved_name>'][0]

#   We will create a brand new model
net = NeuralNet()
net.load(saved_model)

