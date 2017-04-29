import os
import subprocess

if __name__ == "__main__":
	a = 1
	b = 1

	while a < 22:
		os.system("python sample_solver.py /Users/KennyKao1/Desktop/cs170proj/project_instances/problem" + str(a) + ".in" + " wow" + str(b) + ".out")
		a += 1
		b += 1