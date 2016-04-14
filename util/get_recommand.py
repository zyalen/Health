import numpy

def matrix_factorisation(R, P, Q, K, steps=1000, alpha=0.0002, beta=0.02):
  Q = Q.T
  for step in xrange(steps):
    for i in xrange(len(R)):
      for j in xrange(len(R[i])):
        if R[i][j] > 0:
          eij = R[i][j] - numpy.dot(P[i, :], Q[:, j])
          for k in xrange(K):
            P[i][k] = P[i][k] + alpha * (2 * eij * Q[k][j] - beta * P[i][k])
            Q[k][j] = Q[k][j] + alpha * (2 * eij * P[i][k] - beta * Q[k][j])
    eR = numpy.dot(P, Q)
    e = 0
    for i in xrange(len(R)):
      for j in xrange(len(R[i])):
        if R[i][j] > 0:
          e = e + pow(R[i][j] - numpy.dot(P[i, :], Q[:, j]), 2)
          for k in xrange(K):
            e = e + (beta / 2) * (pow(P[i][k], 2) + pow(Q[k][j], 2))
    if e < 0.001:
      break
  return P, Q.T

def get_recommand(data):
  R = numpy.array(data)
  N = len(R)
  M = len(R[0])
  K = 2

  P = numpy.random.rand(N, K)
  Q = numpy.random.rand(M, K)

  nP, nQ = matrix_factorisation(R, P, Q, K)
  nR = numpy.dot(nP, nQ.T)
  return nR