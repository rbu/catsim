import unittest
import numpy
from catsim import irt
from catsim import cat
from catsim import plot
from catsim import stats
from catsim.simulation import Simulator
from catsim.cat import generate_item_bank
from catsim.stopping import MaxItemStopper, MinErrorStopper
from catsim.selection import MaxInfoSelector, ClusterSelector, LinearSelector, RandomSelector, AStratifiedBBlockingSelector, MaxInfoStratificationSelector, MaxInfoBBlockingSelector, AStratifiedSelector, The54321Selector, RandomesqueSelector, IntervalIntegrationSelector
from catsim.initialization import RandomInitializer, FixedPointInitializer
from catsim.estimation import HillClimbingEstimator, DifferentialEvolutionEstimator


def test_item_bank_generation():
    for items in [
        generate_item_bank(5, '1PL'), generate_item_bank(5, '2PL'), generate_item_bank(5, '3PL'),
        generate_item_bank(
            5,
            '3PL',
            corr=0
        ), generate_item_bank(5, '4PL')
    ]:
        irt.validate_item_bank(items, raise_err=True)

    items = numpy.zeros((100))
    irt.validate_item_bank(items)
    items = irt.normalize_item_bank(items)
    irt.validate_item_bank(items, raise_err=True)


def test_plots():
    from matplotlib.pyplot import close
    initializer = RandomInitializer()
    selector = MaxInfoSelector()
    estimator = HillClimbingEstimator()
    stopper = MaxItemStopper(20)
    s = Simulator(generate_item_bank(100), 10)
    s.simulate(initializer, selector, estimator, stopper)

    for item in s.items[0:10]:
        yield plot.item_curve, item[0], item[1], item[2], item[
            3
        ], 'Test plot', 'icc', False, None, False
        yield plot.item_curve, item[0], item[1], item[2], item[
            3
        ], 'Test plot', 'iic', True, None, False
        yield plot.item_curve, item[0], item[1], item[2], item[
            3
        ], 'Test plot', 'both', True, None, False
        close('all')

    plot.gen3D_dataset_scatter(items=s.items, show=False)
    plot.test_progress(
        title='Test progress',
        simulator=s,
        index=0,
        info=True,
        see=True,
        reliability=True,
        show=False
    )

    # close all plots after testing
    close('all')


def test_stats():
    import numpy.random as nprnd
    for _ in range(10):
        items = generate_item_bank(500)
        stats.coef_variation(items)
        stats.coef_correlation(items)
        stats.covariance(items)
        stats.covariance(items, False)
        stats.scatter_matrix(items)

        random_integers = nprnd.randint(30, size=1000)
        stats.bincount(random_integers)


def one_simulation(items, examinees, initializer, selector, estimator, stopper):
    s = Simulator(items, examinees)
    s.simulate(initializer, selector, estimator, stopper)
    cat.rmse(s.examinees, s.estimations)


def test_simulations():
    examinees = 10
    test_size = 20
    bank_size = 5000

    logistic_models = [
        # '1PL', '2PL',
        '4PL'
    ]
    initializers = [
        RandomInitializer('uniform',
                          (-5, 5)
                          # ), RandomInitializer(
                          #     'normal', (0, 1)
                          ),
        FixedPointInitializer(0)
    ]
    infinite_selectors = [MaxInfoSelector(), RandomSelector(), IntervalIntegrationSelector(0.3)]
    finite_selectors = [
        LinearSelector(
            numpy.random.randint(
                bank_size,
                size=test_size
            )
        ), AStratifiedSelector(test_size), AStratifiedBBlockingSelector(test_size),
        MaxInfoStratificationSelector(test_size), MaxInfoBBlockingSelector(test_size),
        The54321Selector(test_size), RandomesqueSelector(5)
    ]

    estimators = [HillClimbingEstimator(), DifferentialEvolutionEstimator((-8, 8))]
    # FMinEstimator()

    for logistic_model in logistic_models:
        for initializer in initializers:
            for estimator in estimators:
                for stopper in [MaxItemStopper(test_size)]:
                    for selector in finite_selectors:
                        items = generate_item_bank(bank_size, itemtype=logistic_model)
                        yield one_simulation, items, examinees, initializer, selector, estimator, stopper

                for stopper in [MinErrorStopper(.4)]:
                    for selector in infinite_selectors:
                        items = generate_item_bank(bank_size, itemtype=logistic_model)
                        yield one_simulation, items, examinees, initializer, selector, estimator, stopper


def test_cism():
    from sklearn.cluster import KMeans

    examinees = 10
    initializers = [
        RandomInitializer('uniform',
                          (-5, 5)
                          # ), RandomInitializer(
                          #     'normal', (0, 1)
                          ),
        FixedPointInitializer(0)
    ]
    estimators = [HillClimbingEstimator(), DifferentialEvolutionEstimator((-8, 8))]
    # , FMinEstimator()
    stoppers = [MaxItemStopper(20), MinErrorStopper(.4)]

    for initializer in initializers:
        for estimator in estimators:
            for stopper in stoppers:
                items = generate_item_bank(5000)
                clusters = list(KMeans(n_clusters=8).fit_predict(items))
                ClusterSelector.weighted_cluster_infos(0, items, clusters)
                ClusterSelector.avg_cluster_params(items, clusters)
                selector = ClusterSelector(clusters=clusters, r_max=.2)
                yield one_simulation, items, examinees, initializer, selector, estimator, stopper


if __name__ == '__main__':
    unittest.main()
