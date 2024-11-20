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
wps_dir = '/work2/07655/tg869546/stampede3/WRF-4.5.2/WPS/WPS-4.5' #* Update for where your WPS files are
ungrib_prefix = 'GFS' #* Update for what your meteorology IC/BC files are


for seq, start_date, end_date in zip(seqs, start_dates, end_dates):
     with open(f'namelist.{seq}') as fl:
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
        fl.write(f"opt_metgrid_tbl_path         = '{wps_dir}/metgrid/',\n")
        fl.write(f"/\n")
