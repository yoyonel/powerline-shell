#!/bin/bash
# curl -H "Content-Type: application/json" -X POST -d '{"username":"xyz","password":"xyz"}'  http://127.0.0.1:8080/api/v1/addrecord/test

curl "http://127.0.0.1:8080/api/v1/addrecord/test" \
-H "Accept: application/json" \
-H "Content-Type:application/json" \
--data @<(cat <<EOF
{
  "me": "$USER",
  "something": $(date +%s)
  }
EOF
)