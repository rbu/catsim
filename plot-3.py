from catsim.cat import generate_item_bank
from catsim import plot
from catsim.initialization import RandomInitializer
from catsim.selection import MaxInfoSelector
from catsim.estimation import HillClimbingEstimator
from catsim.stopping import MaxItemStopper
from catsim.simulation import Simulator

initializer = RandomInitializer()
selector = MaxInfoSelector()
estimator = HillClimbingEstimator()
stopper = MaxItemStopper(20)
s = Simulator(generate_item_bank(100), 10)
s.simulate(initializer, selector, estimator, stopper)
plot.test_progress(simulator=s, index=0)
plot.test_progress(simulator=s, index=0, true_theta=s.examinees[0], info=True, var=True, see=True)