
from qiskit_algorithms.utils import algorithm_globals
from qiskit_algorithms.optimizers import COBYLA
from qiskit_algorithms import NumPyMinimumEigensolver, QAOA, SamplingVQE
from qamelpo import PortfolioOptimization
from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit import Aer, execute
from qiskit.circuit import Parameter
from qiskit_aer.primitives import Sampler
from qiskit.circuit.library import TwoLocal



algorithm_globals.random_seed = 1234

cobyla = COBYLA()
cobyla.set_options(maxiter=500)
def qaoa_optimize(portfolio:PortfolioOptimization):
    qp = portfolio.to_quadratic_program()
    qaoa_mes = QAOA(sampler=Sampler(), optimizer=cobyla, reps=3)
    qaoa = MinimumEigenOptimizer(qaoa_mes)
    result = qaoa.solve(qp)
    return result




def vqe_optimize(portfolio:PortfolioOptimization):
    qp = portfolio.to_quadratic_program()
    ry = TwoLocal(num_qubits=5, rotation_blocks="ry", entanglement_blocks="cz", reps=2, entanglement="full")
    # ry = portfolio_antz(num_qubits=2)
    # print(ry.num_qubits)
    svqe_mes = SamplingVQE(sampler=Sampler(), ansatz=ry, optimizer=cobyla)
    svqe = MinimumEigenOptimizer(svqe_mes)
    result = svqe.solve(qp)
    return result
    


def classical_optimizer(portfolio:PortfolioOptimization): 
    qp = portfolio.to_quadratic_program()
    exact_mes = NumPyMinimumEigensolver()
    exact_eigensolver = MinimumEigenOptimizer(exact_mes)

    result = exact_eigensolver.solve(qp)
    return result

    
    
