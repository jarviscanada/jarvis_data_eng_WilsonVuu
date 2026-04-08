#!/bin/bash
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
vmstat_mb=$(vmstat --unit M)

memory_free=$(echo "$vmstat_mb" | tail -1 | awk '{print $4}' | xargs)
cpu_idle=$(echo "$vmstat_mb" | tail -1 | awk '{print $15}' | xargs)
cpu_kernel=$(echo "$vmstat_mb" | tail -1 | awk '{print $14}' | xargs)
disk_io=$(echo "$vmstat_mb" | tail -1 | awk '{print $9+$10}' | xargs) # Total disk I/O (blocks read + blocks written per second)
disk_available=$(df -BM / | awk 'NR==2 {print $4+0}' | xargs) # +0 is a shortcut to forcing it as a number
timestamp=$(date -u '+%Y-%m-%d %H:%M:%S')

host_id="(SELECT id FROM host_info WHERE hostname='$hostname')"

insert_stmt="INSERT INTO host_usage(
    timestamp,
    host_id,
    memory_free,
    cpu_idle,
    cpu_kernel,
    disk_io,
    disk_available
) VALUES (
    '$timestamp',
    $host_id,
    $memory_free,
    $cpu_idle,
    $cpu_kernel,
    $disk_io,
    $disk_available
);"

export PGPASSWORD=$psql_password
psql -h $psql_host -p $psql_port -d $db_name -U $psql_user -c "$insert_stmt"
exit $?