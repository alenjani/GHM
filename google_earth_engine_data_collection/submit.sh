#!/bin/bash
#SBATCH --job-name=try0.job
#SBATCH --output=output0.out
#SBATCH --error=error0.err
#SBATCH --time=2-00:00
#SBATCH --ntasks=25
#SBATCH --qos=normal
#SBATCH --mail-type=ALL
#  module load python/3.6.1

# module load anaconda/5.0.0-py36
#  module laod devel
#  module load openmpi/4.0.0

module load py-scikit-learn/0.19.1_py36

module load py-mpi4py/3.0.3_py36

module load py-numpy/1.18.1_py36

module load python/3.6.1

#  source ~/MPIpool/bin/activate


mpiexec python3.6 parallel_main.py
