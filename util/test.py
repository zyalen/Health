import get_recommand

R = [
  [5, 3, 0, 1],
  [4, 0, 0, 1],
  [1, 1, 0, 5],
  [1, 0, 0, 4],
  [0, 0, 0, 0],
]

nR = get_recommand.get_recommand(R)
print nR[1]
