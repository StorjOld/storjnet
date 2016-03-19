#!/usr/bin/env bash

time env/bin/python benchmark/filterupdates.py --swarm_size=512\
        --test_timedelta=8.0 --test_count=75 --quasar_size=512\
        --quasar_depth=2 --quasar_ttl=64 --quasar_freshness=66\
        --quasar_refresh_time=60 --quasar_extra_propagations=30\
        &> benchmark/filterupdates_sub_freq_test_a.log

time env/bin/python benchmark/filterupdates.py --swarm_size=512\
        --test_timedelta=4.0 --test_count=150 --quasar_size=512\
        --quasar_depth=2 --quasar_ttl=64 --quasar_freshness=66\
        --quasar_refresh_time=60 --quasar_extra_propagations=30\
        &> benchmark/filterupdates_sub_freq_test_b.log

time env/bin/python benchmark/filterupdates.py --swarm_size=512\
        --test_timedelta=2.0 --test_count=300 --quasar_size=512\
        --quasar_depth=2 --quasar_ttl=64 --quasar_freshness=66\
        --quasar_refresh_time=60 --quasar_extra_propagations=30\
        &> benchmark/filterupdates_sub_freq_test_c.log

time env/bin/python benchmark/filterupdates.py --swarm_size=512\
        --test_timedelta=1.0 --test_count=600 --quasar_size=512\
        --quasar_depth=2 --quasar_ttl=64 --quasar_freshness=66\
        --quasar_refresh_time=60 --quasar_extra_propagations=30\
        &> benchmark/filterupdates_sub_freq_test_d.log

time env/bin/python benchmark/filterupdates.py --swarm_size=512\
        --test_timedelta=0.5 --test_count=1200 --quasar_size=512\
        --quasar_depth=2 --quasar_ttl=64 --quasar_freshness=66\
        --quasar_refresh_time=60 --quasar_extra_propagations=30\
        &> benchmark/filterupdates_sub_freq_test_e.log

time env/bin/python benchmark/filterupdates.py --swarm_size=512\
        --test_timedelta=0.25 --test_count=2400 --quasar_size=512\
        --quasar_depth=2 --quasar_ttl=64 --quasar_freshness=66\
        --quasar_refresh_time=60 --quasar_extra_propagations=30\
        &> benchmark/filterupdates_sub_freq_test_f.log

time env/bin/python benchmark/filterupdates.py --swarm_size=512\
        --test_timedelta=0.125 --test_count=4800 --quasar_size=512\
        --quasar_depth=2 --quasar_ttl=64 --quasar_freshness=66\
        --quasar_refresh_time=60 --quasar_extra_propagations=30\
        &> benchmark/filterupdates_sub_freq_test_g.log

time env/bin/python benchmark/filterupdates.py --swarm_size=512\
        --test_timedelta=0.0625 --test_count=9600 --quasar_size=512\
        --quasar_depth=2 --quasar_ttl=64 --quasar_freshness=66\
        --quasar_refresh_time=60 --quasar_extra_propagations=30\
        &> benchmark/filterupdates_sub_freq_test_h.log

time env/bin/python benchmark/filterupdates.py --swarm_size=512\
        --test_timedelta=0.03125 --test_count=19200 --quasar_size=512\
        --quasar_depth=2 --quasar_ttl=64 --quasar_freshness=66\
        --quasar_refresh_time=60 --quasar_extra_propagations=30\
        &> benchmark/filterupdates_sub_freq_test_i.log
