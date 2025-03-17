import numpy as np

# Parameters
T = 1.0  # Time to maturity
N = 1000  # Number of time steps
M = 100000  # Number of Monte Carlo simulations
dt = T / N  # Time step

# Asset parameters
mu_V, sigma_V = 0.05, 0.2
mu_E, sigma_E = 0.03, 0.15
mu_P, sigma_P = 0.02, 0.10

# Initial values
V0, E0, P0 = 100, 50, 30
K = 100  # Strike price
r = 0.03  # Risk-free rate

# Correlation matrix and Cholesky decomposition
corr_matrix = np.array([[1.0, 0.5, 0.2],
                        [0.5, 1.0, 0.3],
                        [0.2, 0.3, 1.0]])
L = np.linalg.cholesky(corr_matrix)

# Generate correlated Brownian motions
Z = np.random.randn(N, M, 3)
dW = np.dot(Z, L.T) * np.sqrt(dt)

# Initialize paths (correct: explicitly use float)
V, E, P = np.full(M, V0, dtype=np.float64), np.full(M, E0, dtype=np.float64), np.full(M, P0, dtype=np.float64)


# Simulate paths
for i in range(N):
    V *= np.exp((mu_V - 0.5 * sigma_V ** 2) * dt + sigma_V * dW[i,:,0])
    E *= np.exp((mu_E - 0.5 * sigma_E ** 2) * dt + sigma_E * dW[i,:,1])
    P *= np.exp((mu_P - 0.5 * sigma_P ** 2) * dt + sigma_P * dW[i,:,2])

# Compute option payoff
payoff = np.maximum(V - K, 0)
option_price = np.exp(-r * T) * np.mean(payoff)

print(f"Estimated Option Price: {option_price:.2f}")

