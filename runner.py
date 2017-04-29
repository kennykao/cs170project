import os
import subprocess

if __name__ == "__main__":
	a = 14
	b = 14

	while a < 15:
		os.system("python sample_solver.py /Users/christinemunar/Documents/Spring2017/CS170/PhaseII-Proj/cs170project/project_instances/problem" + str(a) + ".in" + " problem" + str(b) + ".out")
		# os.system("python sample_solver.py /Users/KennyKao1/Desktop/cs170proj/project_instances/problem" + str(a) + ".in" + " wow" + str(b) + ".out")
		a += 1
		b += 1