import numpy as np
import matplotlib.pyplot as plt
from catsim.estimation import *
from catsim.cat import generate_item_bank

test_size = 20
randBinList = lambda n: [np.random.randint(0,2) for b in range(1,n+1)]
items = generate_item_bank(20)
items = items[items[:,1].argsort()] # order by difficulty ascending
r0 = [1] * 7 + [0] * 13
r1 = [1] * 10 + [0] * 10
r2 = [1] * 15 + [0] * 5
response_vectors = [r0, r1, r2]
thetas = np.arange(-6.,6.,.1)

for estimator in [FMinEstimator(), DifferentialEvolutionEstimator((-8, 8)), HillClimbingEstimator()]:
    plt.figure()

    for response_vector in response_vectors:
        ll_line = [irt.logLik(theta, response_vector, items) for theta in thetas]
        max_LL = estimator.estimate(response_vector, items, 0)
        best_theta = irt.logLik(max_LL, response_vector, items)
        plt.plot(thetas, ll_line)
        plt.plot(max_LL, best_theta, 'o', label = str(sum(response_vector)) + ' correct, '+r'$\hat{\theta} \approx $' + format(round(max_LL, 5)))
        plt.xlabel(r'$\theta$', size=16)
        plt.ylabel(r'$\log L(\theta)$', size=16)
        plt.title('MLE -- {0} ({1} avg. evals)'.format(type(estimator).__name__, round(estimator.avg_evaluations)))
        plt.legend(loc='best')

    plt.show()