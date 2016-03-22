#!/usr/bin/env bash

time env/bin/python benchmark/filterupdates.py --swarm_size=400\
        --test_timedelta=0.125 --test_count=4800 --quasar_size=512\
        --quasar_depth=2 --quasar_ttl=64 --quasar_freshness=66\
        --quasar_refresh_time=60 --quasar_extra_propagations=0\
        &> benchmark/filterupdates_quasar_refresh_a.json

time env/bin/python benchmark/filterupdates.py --swarm_size=400\
        --test_timedelta=0.125 --test_count=4800 --quasar_size=512\
        --quasar_depth=2 --quasar_ttl=64 --quasar_freshness=66\
        --quasar_refresh_time=60 --quasar_extra_propagations=2\
        &> benchmark/filterupdates_quasar_refresh_b.json

time env/bin/python benchmark/filterupdates.py --swarm_size=400\
        --test_timedelta=0.125 --test_count=4800 --quasar_size=512\
        --quasar_depth=2 --quasar_ttl=64 --quasar_freshness=66\
        --quasar_refresh_time=60 --quasar_extra_propagations=4\
        &> benchmark/filterupdates_quasar_refresh_c.json

time env/bin/python benchmark/filterupdates.py --swarm_size=400\
        --test_timedelta=0.125 --test_count=4800 --quasar_size=512\
        --quasar_depth=2 --quasar_ttl=64 --quasar_freshness=66\
        --quasar_refresh_time=60 --quasar_extra_propagations=6\
        &> benchmark/filterupdates_quasar_refresh_d.json

time env/bin/python benchmark/filterupdates.py --swarm_size=400\
        --test_timedelta=0.125 --test_count=4800 --quasar_size=512\
        --quasar_depth=2 --quasar_ttl=64 --quasar_freshness=66\
        --quasar_refresh_time=60 --quasar_extra_propagations=8\
        &> benchmark/filterupdates_quasar_refresh_e.json

time env/bin/python benchmark/filterupdates.py --swarm_size=400\
        --test_timedelta=0.125 --test_count=4800 --quasar_size=512\
        --quasar_depth=2 --quasar_ttl=64 --quasar_freshness=66\
        --quasar_refresh_time=60 --quasar_extra_propagations=10\
        &> benchmark/filterupdates_quasar_refresh_f.json

time env/bin/python benchmark/filterupdates.py --swarm_size=400\
        --test_timedelta=0.125 --test_count=4800 --quasar_size=512\
        --quasar_depth=2 --quasar_ttl=64 --quasar_freshness=66\
        --quasar_refresh_time=60 --quasar_extra_propagations=12\
        &> benchmark/filterupdates_quasar_refresh_g.json

time env/bin/python benchmark/filterupdates.py --swarm_size=400\
        --test_timedelta=0.125 --test_count=4800 --quasar_size=512\
        --quasar_depth=2 --quasar_ttl=64 --quasar_freshness=66\
        --quasar_refresh_time=60 --quasar_extra_propagations=14\
        &> benchmark/filterupdates_quasar_refresh_h.json

time env/bin/python benchmark/filterupdates.py --swarm_size=400\
        --test_timedelta=0.125 --test_count=4800 --quasar_size=512\
        --quasar_depth=2 --quasar_ttl=64 --quasar_freshness=66\
        --quasar_refresh_time=60 --quasar_extra_propagations=16\
        &> benchmark/filterupdates_quasar_refresh_i.json

time env/bin/python benchmark/filterupdates.py --swarm_size=400\
        --test_timedelta=0.125 --test_count=4800 --quasar_size=512\
        --quasar_depth=2 --quasar_ttl=64 --quasar_freshness=66\
        --quasar_refresh_time=60 --quasar_extra_propagations=18\
        &> benchmark/filterupdates_quasar_refresh_j.json
