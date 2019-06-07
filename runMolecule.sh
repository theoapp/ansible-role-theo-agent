#!/usr/bin/env bash
SCENARIOS="default signature custom-bin-file custom-config-file custom-config-dir"

MUST_FAIL="centos6:custom-config-file centos6:custom-config-dir"

function has_right_to_fail {
    for i in ${MUST_FAIL}; do
        if [ "${MOLECULE_DISTRO}:${1}" = "${i}" ]; then
            return 1
        fi
    done
    return 0
}

for scenario in ${SCENARIOS}; do
    molecule test -s ${scenario}
    RETURN_SCENARIO=$?
    has_right_to_fail ${scenario}
    RIGHT_TO_FAIL=$?
    if [ ${RETURN_SCENARIO} -gt 0 ] && [ ${RIGHT_TO_FAIL} -eq 0 ]; then
        exit ${RETURN_SCENARIO}
    fi;

    if [ ${RETURN_SCENARIO} -eq 0 ] && [ ${RIGHT_TO_FAIL} -eq 1 ]; then
        echo "${MOLECULE_DISTRO} on ${scenario} must fail"
        exit 1;
    fi
done
