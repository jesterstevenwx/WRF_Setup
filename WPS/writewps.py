## Script for writing the namelists for WPS

seqs = ['wps_geoungrib', 'metgrid']
start_dates = ['YYYY-MM-DD_HH:00:00','YYYY-MM-DD_HH:00:00'] #! must be strings and must be in this format
end_dates = ['YYYY-MM-DD_HH:00:00','YYYY-MM-DD_HH:00:00'] #! must be strings and must be in this format
output_dir = './' # where you want to output geogrid/metgrid files
e_we_d01 = 443 #! Do not change. CONUS domain
e_sn_d01 = 266 #! Do not change. CONUS domain
e_we_d02 = 301 #* Update for the project
e_sn_d02 = 256 #* Update for the project
parent_grid_ratio_d02 = 15 #* Update for project (dx and dy for d02 will be d01_dx/grid_ratio or d01_dy/grid_ratio)
i_parent_start_d02 = 372 #* Update for the project (use WRF_Domain_Wizard)
j_parent_start_d02 = 154 #* Update for the project (use WRF_Domain_Wizard)
dxy = 12000 #! Do not change. CONUS domain/base dx and dy for nests in meters
ref = (40, -97) #! Do not change. CONUS domain
true_lats = (33, 45) #! Do not change. CONUS domain.
wps_dir = '$WORK/WPS' #* Update for where your WPS files are
ungrib_prefix = 'GFS' #* Update for what your meteorology IC/BC files are
merra_pgm_dir = '../merra2wps'
chem_dir = '$HOME/work/chem-files'
vtable = 'Vtable.GFS'
bc_ic = '<insert path to bc/ic files here>'
if ungrib_prefix == 'MERRA':
   days = ["'YYYYMMDD',"] #! Update for project, must be strings in this format
   dates = ["'YYYY-MM-DD',"] #! Update for project, must be strings in this format
   ananv_files = [*(f"'MERRA2_400.inst6_3d_ana_Nv.{i}.nc4'," for i in days)]
   ananp_files = [*(f"'MERRA2_400.inst6_3d_ana_Np.{i}.nc4'," for i in days)]
   slv_files = [*(f"'MERRA2_400.tavg1_2d_slv_Nx.{i}.nc4'," for i in days)]
   ocn_files = [*(f"'MERRA2_400.tavg1_2d_ocn_Nx.{i}.nc4'," for i in days)]
   lnd_files = [*(f"'MERRA2_400.tavg1_2d_lnd_Nx.{i}.nc4'," for i in days)]
   num_days = len(days)

for seq, start_date, end_date in zip(seqs, start_dates, end_dates):
     with open(f'namelist.{seq}', 'a') as fl:
         fl.write(f"&share\n")
         fl.write(f"wrf_core = 'ARW',\n")
         fl.write(f"max_dom = 2,\n")
         fl.write(f"start_date = '{start_date}',\n")
         fl.write(f"            '{start_date}',\n")
         fl.write(f"            '{start_date}',\n")
         fl.write(f"            '{start_date}',\n")
         fl.write(f"end_date   = '{end_date}',\n")
         fl.write(f"            '{end_date}',\n")
         fl.write(f"            '{end_date}',\n")
         fl.write(f"            '{end_date}',\n")
         fl.write(f"interval_seconds = 21600,\n")
         fl.write(f"io_form_geogrid = 2,\n")
         fl.write(f"opt_output_from_geogrid_path = '{output_dir}',\n")
         fl.write(f"debug_level = 0,\n")
         fl.write(f"/\n")
         fl.write(f"\n")
         fl.write(f"&geogrid\n")
         fl.write(f"parent_id         =   1, 1, 2, 3,\n")
         fl.write(f"parent_grid_ratio =   1, {parent_grid_ratio_d02}, 5, 5,\n")
         fl.write(f"i_parent_start    =   1, {i_parent_start_d02}, 164, 77,\n")
         fl.write(f"j_parent_start    =   1, {j_parent_start_d02}, 90, 80,\n")
         fl.write(f"s_we              =   1,   1,   1,   1,\n")
         fl.write(f"e_we              =  {e_we_d01}, {e_we_d02}, 161, 161,\n")
         fl.write(f"s_sn              =   1,   1,   1,   1,\n")
         fl.write(f"e_sn              =  {e_sn_d01}, {e_sn_d02}, 161, 161,\n")
         fl.write(f"geog_data_res     = '30s','30s','30s', '30s',\n")
         fl.write(f"dx        = {dxy},\n")
         fl.write(f"dy        = {dxy},\n")
         fl.write(f"map_proj  = 'lambert',\n")
         fl.write(f"ref_lat   = {ref[0]},\n")
         fl.write(f"ref_lon   = {ref[1]},\n")
         fl.write(f"truelat1  = {true_lats[0]},\n")
         fl.write(f"truelat2  = {true_lats[1]},\n")
         fl.write(f"stand_lon = {ref[1]},\n")
         fl.write(f"geog_data_path = '/work2/07655/tg869546/stampede3/geog/WPS_GEOG/'\n")
         fl.write(f"opt_geogrid_tbl_path = '{wps_dir}/geogrid'\n")
         fl.write(f"/\n")
         fl.write(f"\n")
         fl.write(f"&ungrib\n")
         fl.write(f"out_format = 'WPS',\n")
         fl.write(f"prefix     = '{ungrib_prefix}',\n")
         fl.write(f"/\n")
         fl.write(f"\n")
         fl.write(f"&metgrid\n")
         fl.write(f"fg_name         = '{ungrib_prefix}'\n")
         fl.write(f"constants_name  = ''\n")
         fl.write(f"io_form_metgrid = 2,\n")
         fl.write(f"opt_output_from_metgrid_path = '{output_dir}',\n")
         if ungrib_prefix == 'MERRA':
            fl.write(f"opt_metgrid_tbl_path         = './',\n")
         else:
            fl.write(f"opt_metgrid_tbl_path         = '{wps_dir}/metgrid/',\n")
         fl.write(f"/\n")

with open('wps_ghg.sh','a') as fl:
   fl.write(f"#!/bin/bash -l\n")
   fl.write(f"#SBATCH -J WPS_GHG\n")
   fl.write(f"#SBATCH -e WPS_GHG.e.%j\n")
   fl.write(f"#SBATCH -o WPS_GHG.o.%j\n")
   fl.write(f"#SBATCH -n 1       # Requests cpus\n")
   fl.write(f"#SBATCH -N 1       # Requested nodes\n")
   fl.write(f"#SBATCH -p skx # Queue name\n")
   fl.write(f"#SBATCH -t 48:00:00       # Run time (hh:mm:ss) - 1.5 hours\n")
   fl.write(f"#SBATCH --mail-user=steve@belumenus.com\n")
   fl.write(f"#SBATCH --mail-type=all\n")
   fl.write(f"\n")
   fl.write(f"ln -sf {wps_dir}/*.exe .\n")
   fl.write(f"ln -sf namelist.wps_geoungrib namelist.wps\n")
   fl.write(f"./geogrid.exe >& geogrid.log\n")
   fl.write(f"\n")
   if ungrib_prefix == 'MERRA':
      fl.write(f"ln -sf {merra_pgm_dir}/*.TBL .\n")
      fl.write(f"ln -sf {merra_pgm_dir}/bin/Debug/* .\n")
      fl.write(f"ln -sf {chem_dir}/merra-aerosols/*.nc4 .\n")
      fl.write(f"merra2wrf namelist.merra2wrf\n")
      fl.write(f"\n")
   else:
      fl.write(f"ln -sf {wps_dir}/link_grib.csh .\n")
      fl.write(f"ln -sf {wps_dir}/ungrib/Variable_Tables/{vtable} .\n")
      fl.write(f"ln -sf {chem_dir}/wrf* .\n")
      fl.write(f"link_grib.csh {bc_ic}/\n")
      fl.write(f"./ungrib.exe >& ungrib.log\n")
      fl.write(f"\n")
   fl.write(f"ln -sf namelist.metgrid namelist.wps\n")
   fl.write(f"./metgrid.exe >& metgrid.log\n")
   fl.write(f"\n")

if ungrib_prefix == 'MERRA':
   with open('namelist.merra2wrf','a') as fl:
      fl.write(f"&input\n")
      fl.write(f"    outputDirectory = './',\n")
      fl.write(f"    merraDirectory = './',\n")
      fl.write(f"    merraFormat_const_2d_asm_Nx = 2,\n")
      fl.write(f"    merraFile_const_2d_asm_Nx = 'MERRA2_101.const_2d_asm_Nx.00000000.nc4',\n")
      fl.write(f"    numberOfDays={num_days},\n")
      fl.write(f"    !withAerosol=1,\n")
      for i, date in enumerate(dates):
         fl.write(f"    merraDates({i+1})= {date}\n")
      fl.write(f"    merraFormat_inst6_3d_ana_Nv = 2,\n")
      for i, ananv in enumerate(ananv_files):
         fl.write(f"    merraFiles_inst6_3d_ana_Nv({i+1}) = {ananv}\n")
      fl.write(f"    merraFormat_inst6_3d_ana_Np = 2,\n")
      for i, ananp in enumerate(ananp_files):
         fl.write(f"    merraFiles_inst6_3d_ana_Np({i+1}) = {ananp}\n")
      fl.write(f"    merraFormat_tavg1_2d_slv_Nx = 2,\n")
      for i, slv in enumerate(slv_files):
         fl.write(f"    merraFiles_tavg1_2d_slv_Nx({i+1}) = {slv},\n")
      fl.write(f"    merraFormat_tavg1_2d_ocn_Nx = 2,\n")
      for i, ocn in enumerate(ocn_files):
         fl.write(f"    merraFiles_tavg1_2d_ocn_Nx({i+1}) = {ocn}\n")
      fl.write(f"    merraFormat_tavg1_2d_lnd_Nx = 2,\n")
      for i, lnd in enumerate(lnd_files):
         fl.write(f"    merraFiles_tavg1_2d_lnd_Nx({i+1}) = {lnd},\n")
      fl.write(f"    !merraFormat_inst3_3d_aer_Nv = 2,\n")
      fl.write(f"    !merraFiles_inst3_3d_aer_Nv(3) = 'MERRA2_400.inst3_3d_aer_Nv.20240712.nc4','MERRA2_400.inst3_3d_aer_Nv.20240713.nc4','MERRA2_400.inst3_3d_aer_Nv.20240714.nc4',\n")
      fl.write(f"/ \n")