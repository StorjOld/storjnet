#!/usr/bin/env bash

#time env/bin/python benchmark/filterupdates.py --swarm_size=400\
#        --test_timedelta=128.0 --test_count=5 --quasar_size=512\
#        --quasar_depth=2 --quasar_ttl=64 --quasar_freshness=66\
#        --quasar_refresh_time=60 --quasar_extra_propagations=10\
#        &> benchmark/filterupdates_sub_freq_test_a.json
#
#time env/bin/python benchmark/filterupdates.py --swarm_size=400\
#        --test_timedelta=64.0 --test_count=9 --quasar_size=512\
#        --quasar_depth=2 --quasar_ttl=64 --quasar_freshness=66\
#        --quasar_refresh_time=60 --quasar_extra_propagations=10\
#        &> benchmark/filterupdates_sub_freq_test_b.json
#
#time env/bin/python benchmark/filterupdates.py --swarm_size=400\
#        --test_timedelta=32.0 --test_count=19 --quasar_size=512\
#        --quasar_depth=2 --quasar_ttl=64 --quasar_freshness=66\
#        --quasar_refresh_time=60 --quasar_extra_propagations=10\
#        &> benchmark/filterupdates_sub_freq_test_c.json
#
#time env/bin/python benchmark/filterupdates.py --swarm_size=400\
#        --test_timedelta=16.0 --test_count=38 --quasar_size=512\
#        --quasar_depth=2 --quasar_ttl=64 --quasar_freshness=66\
#        --quasar_refresh_time=60 --quasar_extra_propagations=10\
#        &> benchmark/filterupdates_sub_freq_test_d.json
#
#time env/bin/python benchmark/filterupdates.py --swarm_size=400\
#        --test_timedelta=8.0 --test_count=75 --quasar_size=512\
#        --quasar_depth=2 --quasar_ttl=64 --quasar_freshness=66\
#        --quasar_refresh_time=60 --quasar_extra_propagations=10\
#        &> benchmark/filterupdates_sub_freq_test_e.json
#
#time env/bin/python benchmark/filterupdates.py --swarm_size=400\
#        --test_timedelta=4.0 --test_count=150 --quasar_size=512\
#        --quasar_depth=2 --quasar_ttl=64 --quasar_freshness=66\
#        --quasar_refresh_time=60 --quasar_extra_propagations=10\
#        &> benchmark/filterupdates_sub_freq_test_f.json

time env/bin/python benchmark/filterupdates.py --swarm_size=400\
        --test_timedelta=2.0 --test_count=300 --quasar_size=512\
        --quasar_depth=2 --quasar_ttl=64 --quasar_freshness=66\
        --quasar_refresh_time=60 --quasar_extra_propagations=10\
        &> benchmark/filterupdates_sub_freq_test_g.json

time env/bin/python benchmark/filterupdates.py --swarm_size=400\
        --test_timedelta=1.0 --test_count=600 --quasar_size=512\
        --quasar_depth=2 --quasar_ttl=64 --quasar_freshness=66\
        --quasar_refresh_time=60 --quasar_extra_propagations=10\
        &> benchmark/filterupdates_sub_freq_test_h.json

time env/bin/python benchmark/filterupdates.py --swarm_size=400\
        --test_timedelta=0.5 --test_count=1200 --quasar_size=512\
        --quasar_depth=2 --quasar_ttl=64 --quasar_freshness=66\
        --quasar_refresh_time=60 --quasar_extra_propagations=10\
        &> benchmark/filterupdates_sub_freq_test_i.json

time env/bin/python benchmark/filterupdates.py --swarm_size=400\
        --test_timedelta=0.25 --test_count=2400 --quasar_size=512\
        --quasar_depth=2 --quasar_ttl=64 --quasar_freshness=66\
        --quasar_refresh_time=60 --quasar_extra_propagations=10\
        &> benchmark/filterupdates_sub_freq_test_j.json

time env/bin/python benchmark/filterupdates.py --swarm_size=400\
        --test_timedelta=0.125 --test_count=4800 --quasar_size=512\
        --quasar_depth=2 --quasar_ttl=64 --quasar_freshness=66\
        --quasar_refresh_time=60 --quasar_extra_propagations=10\
        &> benchmark/filterupdates_sub_freq_test_k.json

time env/bin/python benchmark/filterupdates.py --swarm_size=400\
        --test_timedelta=0.0625 --test_count=9600 --quasar_size=512\
        --quasar_depth=2 --quasar_ttl=64 --quasar_freshness=66\
        --quasar_refresh_time=60 --quasar_extra_propagations=10\
        &> benchmark/filterupdates_sub_freq_test_l.json
