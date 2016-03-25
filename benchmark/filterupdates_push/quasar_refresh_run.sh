#!/usr/bin/env bash

time env/bin/python benchmark/filterupdates.py --swarm_size=400\
        --test_timedelta=0.125 --test_count=4800 --quasar_size=512\
        --quasar_depth=2 --quasar_ttl=64 --quasar_freshness=16\
        --quasar_refresh_time=10 --quasar_extra_propagations=0\
        &> benchmark/filterupdates_push/quasar_refresh_a.json

time env/bin/python benchmark/filterupdates.py --swarm_size=400\
        --test_timedelta=0.125 --test_count=4800 --quasar_size=512\
        --quasar_depth=2 --quasar_ttl=64 --quasar_freshness=26\
        --quasar_refresh_time=20 --quasar_extra_propagations=0\
        &> benchmark/filterupdates_push/quasar_refresh_b.json

time env/bin/python benchmark/filterupdates.py --swarm_size=400\
        --test_timedelta=0.125 --test_count=4800 --quasar_size=512\
        --quasar_depth=2 --quasar_ttl=64 --quasar_freshness=36\
        --quasar_refresh_time=30 --quasar_extra_propagations=0\
        &> benchmark/filterupdates_push/quasar_refresh_c.json

time env/bin/python benchmark/filterupdates.py --swarm_size=400\
        --test_timedelta=0.125 --test_count=4800 --quasar_size=512\
        --quasar_depth=2 --quasar_ttl=64 --quasar_freshness=46\
        --quasar_refresh_time=40 --quasar_extra_propagations=0\
        &> benchmark/filterupdates_push/quasar_refresh_d.json

time env/bin/python benchmark/filterupdates.py --swarm_size=400\
        --test_timedelta=0.125 --test_count=4800 --quasar_size=512\
        --quasar_depth=2 --quasar_ttl=64 --quasar_freshness=56\
        --quasar_refresh_time=50 --quasar_extra_propagations=0\
        &> benchmark/filterupdates_push/quasar_refresh_e.json

time env/bin/python benchmark/filterupdates.py --swarm_size=400\
        --test_timedelta=0.125 --test_count=4800 --quasar_size=512\
        --quasar_depth=2 --quasar_ttl=64 --quasar_freshness=66\
        --quasar_refresh_time=60 --quasar_extra_propagations=0\
        &> benchmark/filterupdates_push/quasar_refresh_f.json

time env/bin/python benchmark/filterupdates.py --swarm_size=400\
        --test_timedelta=0.125 --test_count=4800 --quasar_size=512\
        --quasar_depth=2 --quasar_ttl=64 --quasar_freshness=76\
        --quasar_refresh_time=70 --quasar_extra_propagations=0\
        &> benchmark/filterupdates_push/quasar_refresh_g.json

time env/bin/python benchmark/filterupdates.py --swarm_size=400\
        --test_timedelta=0.125 --test_count=4800 --quasar_size=512\
        --quasar_depth=2 --quasar_ttl=64 --quasar_freshness=86\
        --quasar_refresh_time=80 --quasar_extra_propagations=0\
        &> benchmark/filterupdates_push/quasar_refresh_h.json

time env/bin/python benchmark/filterupdates.py --swarm_size=400\
        --test_timedelta=0.125 --test_count=4800 --quasar_size=512\
        --quasar_depth=2 --quasar_ttl=64 --quasar_freshness=96\
        --quasar_refresh_time=90 --quasar_extra_propagations=0\
        &> benchmark/filterupdates_push/quasar_refresh_i.json

time env/bin/python benchmark/filterupdates.py --swarm_size=400\
        --test_timedelta=0.125 --test_count=4800 --quasar_size=512\
        --quasar_depth=2 --quasar_ttl=64 --quasar_freshness=106\
        --quasar_refresh_time=100 --quasar_extra_propagations=0\
        &> benchmark/filterupdates_push/quasar_refresh_j.json
