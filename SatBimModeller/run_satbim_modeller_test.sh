#!/bin/bash
modeller_path=('C:/git-satbim_internal/SatBimModeller/')
problems_path=('C:/git-satbim_internal/Examples/casm/lod3/Model_segments/')
gid_path=('C:/Program Files/GiD/GiD 12.0.10/')
JOB_ID=1
echo "running modeller..."
python "${modeller_path}"/SatBimModeller.py "$modeller_path" "$problems_path" "$gid_path" $JOB_ID