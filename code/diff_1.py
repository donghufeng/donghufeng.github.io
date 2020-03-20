import numpy as np
import projectq
from projectq.ops import Ry, Rz, Rx, All, Measure


def random_wavefunc(n_qubits, seed=None):
    if seed is not None:
        np.random.seed(seed)
    w = np.random.random((1 << n_qubits)) + 1j * \
        np.random.random((1 << n_qubits))
    return w/np.sqrt(np.vdot(w, w))


def rx(theta):
    return np.array([[np.cos(theta / 2), -1j * np.sin(theta / 2)],
                     [-1j * np.sin(theta / 2), np.cos(theta / 2)]])


def evl(psi0, ops, n_qubits):
    eng = projectq.MainEngine()
    wavefunction = eng.allocate_qureg(n_qubits)
    eng.flush()

    eng.backend.set_wavefunction(psi0, wavefunction)
    ops | wavefunction[0]
    eng.flush()

    psi = eng.backend.cheat()[1]
    All(Measure) | wavefunction
    return psi


n_qubits = 1
psi1 = random_wavefunc(n_qubits)
psi2 = random_wavefunc(n_qubits)
theta = 0.234
delta_theta = 0.001
a = 2.3

y0 = np.vdot(psi2, evl(psi1, Rx(a * theta), n_qubits))
y1 = np.vdot(psi2, evl(psi1, Rx(a * (theta + delta_theta)), n_qubits))

y2 = np.vdot(psi2, rx(a * theta).dot(psi1))
y3 = np.vdot(psi2, rx(a * theta + np.pi).dot(psi1)) / 2 * a
y4 = np.vdot(psi2, rx(a * (theta + delta_theta)).dot(psi1))


print("y0 =    {}".format(y0))
print('np y0 = {}'.format(y2))

print("excepted gradient =    {}".format(
    a * 0.5 * np.vdot(psi2, evl(psi1, Rx(a * theta+np.pi), n_qubits))))
print('np excepted gradient = {}'.format(y3))

print("difference gradient =    {}".format((y1 - y0) / delta_theta))
print('np difference gradient = {}'.format((y4 - y2) / delta_theta))
