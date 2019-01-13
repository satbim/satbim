#!/bin/bash
modeller_path=`pwd`
problems_path=('G:/Gid_new_modeller/satbim_modeller/New_model_11/')
gid_path=('C:/Program Files/GiD/GiD 12.0.10/')
JOB_ID=1
echo "running modeller..."
python ${modeller_path}/SatBimModeller.py "$modeller_path" "$problems_path" "$gid_path" $JOB_ID