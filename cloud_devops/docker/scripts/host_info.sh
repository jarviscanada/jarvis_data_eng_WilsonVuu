psql_host=$1
psql_port=$2
db_name=$3
psql_user=$4
psql_password=$5

if [ "$#" -ne 5 ]; then
    echo "Illegal number of parameters"
    exit 1
fi

hostname=$(hostname -f)
lscpu_out=$(lscpu)



cpu_number=$(echo "$lscpu_out" | egrep "^CPU\\(s\\):" | awk '{print $2}' | xargs)

cpu_architecture=$(echo "$lscpu_out" | egrep "^Architecture:" | awk '{print $2}' | xargs)
cpu_model=$(echo "$lscpu_out" | egrep "^Model name:" | awk -F: '{print $2}' | xargs)
cpu_mhz=$(echo "$lscpu_out" | egrep "^Model name:" | awk -F'@' '{gsub(/[^0-9.]/, "", $2); print $2 * 1000}' | xargs)
#apple silicon show cpu_mhz as empty, set it to 0
cpu_mhz=${cpu_mhz:-0}
l2_cache=$(echo "$lscpu_out" | egrep "^L2 cache:" | awk '{print $3}' | sed 's/K//' | xargs)
#apple silicon does not show l2 cache, so we set it to 0 if not found
l2_cache=${l2_cache:-0}
timestamp=$(date -u '+%Y-%m-%d %H:%M:%S')
total_mem=$(vmstat -s --unit M | egrep "total memory" | awk '{print $1}')

insert_stmt="INSERT INTO host_info (hostname,
cpu_number, cpu_architecture,
cpu_model,
cpu_mhz,
l2_cache,
timestamp,
total_mem) VALUES('$hostname',
$cpu_number,
'$cpu_architecture',
'$cpu_model',
$cpu_mhz,
$l2_cache,
'$timestamp',
$total_mem);"

export PGPASSWORD=$psql_password
psql -h "$psql_host" -p $psql_port -d "$db_name" -U "$psql_user" -c "$insert_stmt"
exit $?