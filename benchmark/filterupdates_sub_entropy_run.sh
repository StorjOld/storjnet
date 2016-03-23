#!/usr/bin/env bash

time env/bin/python benchmark/filterupdates.py --swarm_size=400\
        --test_subscription_entropy=0\
        --test_timedelta=0.125 --test_count=4800 --quasar_size=512\
        --quasar_depth=2 --quasar_ttl=64 --quasar_freshness=126\
        --quasar_refresh_time=120 --quasar_extra_propagations=10\
        &> benchmark/filterupdates_sub_entropy_test_a.json

time env/bin/python benchmark/filterupdates.py --swarm_size=400\
        --test_subscription_entropy=1\
        --test_timedelta=0.125 --test_count=4800 --quasar_size=512\
        --quasar_depth=2 --quasar_ttl=64 --quasar_freshness=126\
        --quasar_refresh_time=120 --quasar_extra_propagations=10\
        &> benchmark/filterupdates_sub_entropy_test_b.json

time env/bin/python benchmark/filterupdates.py --swarm_size=400\
        --test_subscription_entropy=2\
        --test_timedelta=0.125 --test_count=4800 --quasar_size=512\
        --quasar_depth=2 --quasar_ttl=64 --quasar_freshness=126\
        --quasar_refresh_time=120 --quasar_extra_propagations=10\
        &> benchmark/filterupdates_sub_entropy_test_c.json

time env/bin/python benchmark/filterupdates.py --swarm_size=400\
        --test_subscription_entropy=3\
        --test_timedelta=0.125 --test_count=4800 --quasar_size=512\
        --quasar_depth=2 --quasar_ttl=64 --quasar_freshness=126\
        --quasar_refresh_time=120 --quasar_extra_propagations=10\
        &> benchmark/filterupdates_sub_entropy_test_d.json

time env/bin/python benchmark/filterupdates.py --swarm_size=400\
        --test_subscription_entropy=4\
        --test_timedelta=0.125 --test_count=4800 --quasar_size=512\
        --quasar_depth=2 --quasar_ttl=64 --quasar_freshness=126\
        --quasar_refresh_time=120 --quasar_extra_propagations=10\
        &> benchmark/filterupdates_sub_entropy_test_e.json

time env/bin/python benchmark/filterupdates.py --swarm_size=400\
        --test_subscription_entropy=5\
        --test_timedelta=0.125 --test_count=4800 --quasar_size=512\
        --quasar_depth=2 --quasar_ttl=64 --quasar_freshness=126\
        --quasar_refresh_time=120 --quasar_extra_propagations=10\
        &> benchmark/filterupdates_sub_entropy_test_f.json

time env/bin/python benchmark/filterupdates.py --swarm_size=400\
        --test_subscription_entropy=6\
        --test_timedelta=0.125 --test_count=4800 --quasar_size=512\
        --quasar_depth=2 --quasar_ttl=64 --quasar_freshness=126\
        --quasar_refresh_time=120 --quasar_extra_propagations=10\
        &> benchmark/filterupdates_sub_entropy_test_g.json

time env/bin/python benchmark/filterupdates.py --swarm_size=400\
        --test_subscription_entropy=7\
        --test_timedelta=0.125 --test_count=4800 --quasar_size=512\
        --quasar_depth=2 --quasar_ttl=64 --quasar_freshness=126\
        --quasar_refresh_time=120 --quasar_extra_propagations=10\
        &> benchmark/filterupdates_sub_entropy_test_h.json

time env/bin/python benchmark/filterupdates.py --swarm_size=400\
        --test_subscription_entropy=8\
        --test_timedelta=0.125 --test_count=4800 --quasar_size=512\
        --quasar_depth=2 --quasar_ttl=64 --quasar_freshness=126\
        --quasar_refresh_time=120 --quasar_extra_propagations=10\
        &> benchmark/filterupdates_sub_entropy_test_i.json

time env/bin/python benchmark/filterupdates.py --swarm_size=400\
        --test_subscription_entropy=9\
        --test_timedelta=0.125 --test_count=4800 --quasar_size=512\
        --quasar_depth=2 --quasar_ttl=64 --quasar_freshness=126\
        --quasar_refresh_time=120 --quasar_extra_propagations=10\
        &> benchmark/filterupdates_sub_entropy_test_j.json
