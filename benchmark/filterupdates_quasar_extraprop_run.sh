#!/usr/bin/env bash

time env/bin/python benchmark/filterupdates.py --swarm_size=400\
        --test_timedelta=0.125 --test_count=4800 --quasar_size=512\
        --quasar_depth=2 --quasar_ttl=64 --quasar_freshness=126\
        --quasar_refresh_time=120 --quasar_extra_propagations=0\
        &> benchmark/filterupdates_quasar_extraprop_a.json

time env/bin/python benchmark/filterupdates.py --swarm_size=400\
        --test_timedelta=0.125 --test_count=4800 --quasar_size=512\
        --quasar_depth=2 --quasar_ttl=64 --quasar_freshness=126\
        --quasar_refresh_time=120 --quasar_extra_propagations=1\
        &> benchmark/filterupdates_quasar_extraprop_b.json

time env/bin/python benchmark/filterupdates.py --swarm_size=400\
        --test_timedelta=0.125 --test_count=4800 --quasar_size=512\
        --quasar_depth=2 --quasar_ttl=64 --quasar_freshness=126\
        --quasar_refresh_time=120 --quasar_extra_propagations=4\
        &> benchmark/filterupdates_quasar_extraprop_c.json

time env/bin/python benchmark/filterupdates.py --swarm_size=400\
        --test_timedelta=0.125 --test_count=4800 --quasar_size=512\
        --quasar_depth=2 --quasar_ttl=64 --quasar_freshness=126\
        --quasar_refresh_time=120 --quasar_extra_propagations=8\
        &> benchmark/filterupdates_quasar_extraprop_d.json

time env/bin/python benchmark/filterupdates.py --swarm_size=400\
        --test_timedelta=0.125 --test_count=4800 --quasar_size=512\
        --quasar_depth=2 --quasar_ttl=64 --quasar_freshness=126\
        --quasar_refresh_time=120 --quasar_extra_propagations=16\
        &> benchmark/filterupdates_quasar_extraprop_e.json

time env/bin/python benchmark/filterupdates.py --swarm_size=400\
        --test_timedelta=0.125 --test_count=4800 --quasar_size=512\
        --quasar_depth=2 --quasar_ttl=64 --quasar_freshness=126\
        --quasar_refresh_time=120 --quasar_extra_propagations=32\
        &> benchmark/filterupdates_quasar_extraprop_f.json

time env/bin/python benchmark/filterupdates.py --swarm_size=400\
        --test_timedelta=0.125 --test_count=4800 --quasar_size=512\
        --quasar_depth=2 --quasar_ttl=64 --quasar_freshness=126\
        --quasar_refresh_time=120 --quasar_extra_propagations=64\
        &> benchmark/filterupdates_quasar_extraprop_g.json

time env/bin/python benchmark/filterupdates.py --swarm_size=400\
        --test_timedelta=0.125 --test_count=4800 --quasar_size=512\
        --quasar_depth=2 --quasar_ttl=64 --quasar_freshness=126\
        --quasar_refresh_time=120 --quasar_extra_propagations=128\
        &> benchmark/filterupdates_quasar_extraprop_h.json

time env/bin/python benchmark/filterupdates.py --swarm_size=400\
        --test_timedelta=0.125 --test_count=4800 --quasar_size=512\
        --quasar_depth=2 --quasar_ttl=64 --quasar_freshness=126\
        --quasar_refresh_time=120 --quasar_extra_propagations=256\
        &> benchmark/filterupdates_quasar_extraprop_i.json

time env/bin/python benchmark/filterupdates.py --swarm_size=400\
        --test_timedelta=0.125 --test_count=4800 --quasar_size=512\
        --quasar_depth=2 --quasar_ttl=64 --quasar_freshness=126\
        --quasar_refresh_time=120 --quasar_extra_propagations=512\
        &> benchmark/filterupdates_quasar_extraprop_j.json
