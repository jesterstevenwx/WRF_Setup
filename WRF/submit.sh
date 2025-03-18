#/bin/bash -l

for i in {1..6} ## for loop to submit scripts to SLURM
do
	if [ $i -eq 1 ]; then
		JOB_ID=$(sbatch --parsable wrf_ghg_01.sh)
	elif [ $i -ge 2 ] && [ $i -lt 10 ]; then
		JOB_ID=$(sbatch --parsable --dependency=afterok:${JOB_ID:623} wrf_ghg_0${i}.sh)
	else
		JOB_ID=$(sbatch --parsable --dependency=afterok:${JOB_ID:623} wrf_ghg_${i}.sh)
	fi
	echo ${JOB_ID:623}
	sleep 1
done
