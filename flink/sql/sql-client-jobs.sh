#!/bin/bash

${FLINK_HOME}/bin/sql-client.sh  -i ${SQL_CLIENT_HOME}/sql/init.sql -f ${SQL_CLIENT_HOME}/sql/run.sql
