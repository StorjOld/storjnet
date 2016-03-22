#!/usr/bin/env bash

time env/bin/python benchmark/filterupdates.py --swarm_size=400\
        --test_timedelta=0.25 --test_count=2400 --quasar_size=8\
        --quasar_depth=2 --quasar_ttl=64 --quasar_freshness=66\
        --quasar_refresh_time=60 --quasar_extra_propagations=10\
        &> benchmark/filterupdates_quasar_size_a.json

time env/bin/python benchmark/filterupdates.py --swarm_size=400\
        --test_timedelta=0.25 --test_count=2400 --quasar_size=64\
        --quasar_depth=2 --quasar_ttl=64 --quasar_freshness=66\
        --quasar_refresh_time=60 --quasar_extra_propagations=10\
        &> benchmark/filterupdates_quasar_size_b.json

time env/bin/python benchmark/filterupdates.py --swarm_size=400\
        --test_timedelta=0.25 --test_count=2400 --quasar_size=120\
        --quasar_depth=2 --quasar_ttl=64 --quasar_freshness=66\
        --quasar_refresh_time=60 --quasar_extra_propagations=10\
        &> benchmark/filterupdates_quasar_size_c.json

time env/bin/python benchmark/filterupdates.py --swarm_size=400\
        --test_timedelta=0.25 --test_count=2400 --quasar_size=176\
        --quasar_depth=2 --quasar_ttl=64 --quasar_freshness=66\
        --quasar_refresh_time=60 --quasar_extra_propagations=10\
        &> benchmark/filterupdates_quasar_size_d.json

time env/bin/python benchmark/filterupdates.py --swarm_size=400\
        --test_timedelta=0.25 --test_count=2400 --quasar_size=232\
        --quasar_depth=2 --quasar_ttl=64 --quasar_freshness=66\
        --quasar_refresh_time=60 --quasar_extra_propagations=10\
        &> benchmark/filterupdates_quasar_size_e.json

time env/bin/python benchmark/filterupdates.py --swarm_size=400\
        --test_timedelta=0.25 --test_count=2400 --quasar_size=288\
        --quasar_depth=2 --quasar_ttl=64 --quasar_freshness=66\
        --quasar_refresh_time=60 --quasar_extra_propagations=10\
        &> benchmark/filterupdates_quasar_size_f.json

time env/bin/python benchmark/filterupdates.py --swarm_size=400\
        --test_timedelta=0.25 --test_count=2400 --quasar_size=344\
        --quasar_depth=2 --quasar_ttl=64 --quasar_freshness=66\
        --quasar_refresh_time=60 --quasar_extra_propagations=10\
        &> benchmark/filterupdates_quasar_size_g.json

time env/bin/python benchmark/filterupdates.py --swarm_size=400\
        --test_timedelta=0.25 --test_count=2400 --quasar_size=400\
        --quasar_depth=2 --quasar_ttl=64 --quasar_freshness=66\
        --quasar_refresh_time=60 --quasar_extra_propagations=10\
        &> benchmark/filterupdates_quasar_size_h.json

time env/bin/python benchmark/filterupdates.py --swarm_size=400\
        --test_timedelta=0.25 --test_count=2400 --quasar_size=456\
        --quasar_depth=2 --quasar_ttl=64 --quasar_freshness=66\
        --quasar_refresh_time=60 --quasar_extra_propagations=10\
        &> benchmark/filterupdates_quasar_size_i.json

time env/bin/python benchmark/filterupdates.py --swarm_size=400\
        --test_timedelta=0.25 --test_count=2400 --quasar_size=512\
        --quasar_depth=2 --quasar_ttl=64 --quasar_freshness=66\
        --quasar_refresh_time=60 --quasar_extra_propagations=10\
        &> benchmark/filterupdates_quasar_size_j.json
