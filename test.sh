#!/usr/bin/env sh
set -eu
set -o pipefail
#set -x

echo "TESTS MAY TAKE A LONG TIME, PLEASE BE PATIENT"

dir="$(cd "$(dirname $0)"; pwd -P;)"

ret=0
pids=""

for collection in "$@"; do
	cd "${dir}/${collection}"
	for test in sanity units integration; do
		(
			if ! ansible-test "$test" --venv >/dev/null 2>&1; then
				echo "${collection} ${test} FAILED"
				exit 1
			fi
		) &
		pids="$pids $!"
	done
done

for pid in $pids; do
	if ! wait "$pid"; then
		ret=1
	fi
done

[ "$ret" -ne 0 ] || echo "ALL TESTS PASSED"

exit "$ret"
