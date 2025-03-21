## Script that writes out the submision scripts for a multi-stage WRF run. Options at the beginning can be edited to the length and details of the simulation

seqs = ['real', *(x for x in range(1,49))] # must have 'real' at the beginning
days = [20, *(x for x in range(20,32) for _ in (0,1)), *(x for x in range(1,13) for _ in (0,1))]
mons = [*([7] * 25), *([8] * 24)]
hrs = [0, *([0, 12] * 24)]
email = '<put your email here>'
queue = 'skx'
run_time = '48:00:00' #must be in hh:mm:ss format
tasks_per_node = 48
nodes = 4
wrf_dir = '$HOME/work/WRF/run'
met_em_dir = '../WPS'
chem_dir = '$HOME/work/chem-files'
moz_dir = '../mozbc'

for seq, mon, day, hr in zip(seqs, mons, days, hrs):
    with open(f'wrf_ghg_{f"{seq:02}" if isinstance(seq, int) else seq}.sh','a') as fl:
        fl.write(f'#!/bin/bash -l\n')
        fl.write(f'#\n')
        fl.write(f'#SBATCH -J WRF_GHG_{f"{seq:02}" if isinstance(seq, int) else seq.upper()}\n')
        fl.write(f'#SBATCH -e WRF_GHG_{f"{seq:02}" if isinstance(seq, int) else seq.upper()}.e.%j\n')
        fl.write(f'#SBATCH -o WRF_GHG_{f"{seq:02}" if isinstance(seq, int) else seq.upper()}.o.%j\n')
        fl.write(f'#SBATCH --ntasks-per-node {tasks_per_node}\n')
        fl.write(f'#SBATCH -N {nodes}       # skx-dev\n') 
        fl.write(f'#SBATCH -p {queue} # Queue name\n')
        fl.write(f'#SBATCH -t {run_time}       # Run time (hh:mm:ss) - 1.5 hours\n')
        fl.write(f'#SBATCH --mail-user={email}\n')
        fl.write(f'#SBATCH --mail-type=all\n')
        fl.write(f'\n')
        if seq == 'real':
            fl.write(f'ln -sf {wrf_dir}/* .\n')
            fl.write(f'ln -sf {met_em_dir}/met_em* .\n')
            fl.write(f'ln -sf {chem_dir}/wrf* .\n')
            fl.write(f'ln -sf {chem_dir}/hist* .\n')
            fl.write(f'ln -sf namelist.input.real namelist.input\n')
            fl.write(f'ibrun ./real.exe >& real.log\n')
            fl.write(f'mv rsl.out.0000 rsl.out.real\n')
            fl.write(f'mv rsl.error.0000 rsl.error.real\n')
            fl.write(f'\n')
            fl.write(f'cp wrfinput_d01 wrfinput_d01_beforeCT\n')
            fl.write(f'cp wrfbdy_d01 wrfbdy_d01_beforeCT\n')
            fl.write(f'\n')
            fl.write(f'ln -sf {moz_dir}/*2024*.inp .\n')
            fl.write(f'ln -sf {moz_dir}/CO2CAMS*.inp .\n')
            fl.write(f'ln -sf {moz_dir}/mozbc_* .\n')
            fl.write(f'ln -sf {chem_dir}/CH4/CH4_CAMS/cams73_latest_ch4_conc_surface_satellite_inst_2023_00??.nc .\n')
            fl.write(f'./mozbc_ch4 < CH4_2024yearly08.inp >& CH4_d01.log\n')
            fl.write(f'./mozbc_ch4 < CH4_2024yearly08_d02.inp >& CH4_d02.log\n')
            fl.write(f'\n')
            fl.write(f'ln -sf {chem_dir}/CO2_CAMS/cams73*2023* .\n')
            fl.write(f'\n')
            fl.write(f'./mozbc_co2 < CO2CAMS_2024yearly08.inp >& CO2_d01.log\n')
            fl.write(f'./mozbc_co2 < CO2CAMS_2024yearly08_d02.inp >& CO2_d02.log\n')
            fl.write(f'\n')
        else:
            fl.write(f'ln -sf namelist.input.{f"{seq:02}" if isinstance(seq, int) else seq} namelist.input\n')
            if seq > 1:
                fl.write(f'ncatted -O -h -a MMINLU,global,m,c,"MODIFIED_IGBP_MODIS_NOAH" wrfrst_d02_2023-{mon:02}-{day:02}_{hr:02}:00:00 wrfrst_d02_2023-{mon:02}-{day:02}_{hr:02}:00:00\n')
            fl.write(f'\n')
            fl.write('ibrun ./wrf.exe >& wrf.log\n')
            fl.write(f'mv rsl.out.0000 rsl.out.wrf.{f"{seq:02}" if isinstance(seq, int) else seq}\n')
            fl.write(f'mv rsl.error.0000 rsl.error.wrf.{f"{seq:02}" if isinstance(seq, int) else seq}\n')
        fl.write('\n')
        



