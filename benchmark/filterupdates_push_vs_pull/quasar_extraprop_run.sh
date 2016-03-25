#!/usr/bin/env bash

time env/bin/python benchmark/filterupdates.py --swarm_size=400\
        --test_timedelta=2.0 --test_count=300 --quasar_size=512\
        --quasar_pull_filters=true\
        --quasar_depth=2 --quasar_ttl=64 --quasar_freshness=126\
        --quasar_refresh_time=120 --quasar_extra_propagations=0\
        &> benchmark/filterupdates_push_vs_pull/quasar_extraprop_pull_a.json

time env/bin/python benchmark/filterupdates.py --swarm_size=400\
        --test_timedelta=2.0 --test_count=300 --quasar_size=512\
        --quasar_pull_filters=false\
        --quasar_depth=2 --quasar_ttl=64 --quasar_freshness=126\
        --quasar_refresh_time=120 --quasar_extra_propagations=0\
        &> benchmark/filterupdates_push_vs_pull/quasar_extraprop_push_a.json

time env/bin/python benchmark/filterupdates.py --swarm_size=400\
        --test_timedelta=2.0 --test_count=300 --quasar_size=512\
        --quasar_pull_filters=true\
        --quasar_depth=2 --quasar_ttl=64 --quasar_freshness=126\
        --quasar_refresh_time=120 --quasar_extra_propagations=2\
        &> benchmark/filterupdates_push_vs_pull/quasar_extraprop_pull_b.json

time env/bin/python benchmark/filterupdates.py --swarm_size=400\
        --test_timedelta=2.0 --test_count=300 --quasar_size=512\
        --quasar_pull_filters=false\
        --quasar_depth=2 --quasar_ttl=64 --quasar_freshness=126\
        --quasar_refresh_time=120 --quasar_extra_propagations=2\
        &> benchmark/filterupdates_push_vs_pull/quasar_extraprop_push_b.json

time env/bin/python benchmark/filterupdates.py --swarm_size=400\
        --test_timedelta=2.0 --test_count=300 --quasar_size=512\
        --quasar_pull_filters=true\
        --quasar_depth=2 --quasar_ttl=64 --quasar_freshness=126\
        --quasar_refresh_time=120 --quasar_extra_propagations=4\
        &> benchmark/filterupdates_push_vs_pull/quasar_extraprop_pull_c.json

time env/bin/python benchmark/filterupdates.py --swarm_size=400\
        --test_timedelta=2.0 --test_count=300 --quasar_size=512\
        --quasar_pull_filters=false\
        --quasar_depth=2 --quasar_ttl=64 --quasar_freshness=126\
        --quasar_refresh_time=120 --quasar_extra_propagations=4\
        &> benchmark/filterupdates_push_vs_pull/quasar_extraprop_push_c.json

time env/bin/python benchmark/filterupdates.py --swarm_size=400\
        --test_timedelta=2.0 --test_count=300 --quasar_size=512\
        --quasar_pull_filters=true\
        --quasar_depth=2 --quasar_ttl=64 --quasar_freshness=126\
        --quasar_refresh_time=120 --quasar_extra_propagations=6\
        &> benchmark/filterupdates_push_vs_pull/quasar_extraprop_pull_d.json

time env/bin/python benchmark/filterupdates.py --swarm_size=400\
        --test_timedelta=2.0 --test_count=300 --quasar_size=512\
        --quasar_pull_filters=false\
        --quasar_depth=2 --quasar_ttl=64 --quasar_freshness=126\
        --quasar_refresh_time=120 --quasar_extra_propagations=6\
        &> benchmark/filterupdates_push_vs_pull/quasar_extraprop_push_d.json

time env/bin/python benchmark/filterupdates.py --swarm_size=400\
        --test_timedelta=2.0 --test_count=300 --quasar_size=512\
        --quasar_pull_filters=true\
        --quasar_depth=2 --quasar_ttl=64 --quasar_freshness=126\
        --quasar_refresh_time=120 --quasar_extra_propagations=8\
        &> benchmark/filterupdates_push_vs_pull/quasar_extraprop_pull_e.json

time env/bin/python benchmark/filterupdates.py --swarm_size=400\
        --test_timedelta=2.0 --test_count=300 --quasar_size=512\
        --quasar_pull_filters=false\
        --quasar_depth=2 --quasar_ttl=64 --quasar_freshness=126\
        --quasar_refresh_time=120 --quasar_extra_propagations=8\
        &> benchmark/filterupdates_push_vs_pull/quasar_extraprop_push_e.json

time env/bin/python benchmark/filterupdates.py --swarm_size=400\
        --test_timedelta=2.0 --test_count=300 --quasar_size=512\
        --quasar_pull_filters=true\
        --quasar_depth=2 --quasar_ttl=64 --quasar_freshness=126\
        --quasar_refresh_time=120 --quasar_extra_propagations=10\
        &> benchmark/filterupdates_push_vs_pull/quasar_extraprop_pull_f.json

time env/bin/python benchmark/filterupdates.py --swarm_size=400\
        --test_timedelta=2.0 --test_count=300 --quasar_size=512\
        --quasar_pull_filters=false\
        --quasar_depth=2 --quasar_ttl=64 --quasar_freshness=126\
        --quasar_refresh_time=120 --quasar_extra_propagations=10\
        &> benchmark/filterupdates_push_vs_pull/quasar_extraprop_push_f.json

time env/bin/python benchmark/filterupdates.py --swarm_size=400\
        --test_timedelta=2.0 --test_count=300 --quasar_size=512\
        --quasar_pull_filters=true\
        --quasar_depth=2 --quasar_ttl=64 --quasar_freshness=126\
        --quasar_refresh_time=120 --quasar_extra_propagations=12\
        &> benchmark/filterupdates_push_vs_pull/quasar_extraprop_pull_g.json

time env/bin/python benchmark/filterupdates.py --swarm_size=400\
        --test_timedelta=2.0 --test_count=300 --quasar_size=512\
        --quasar_pull_filters=false\
        --quasar_depth=2 --quasar_ttl=64 --quasar_freshness=126\
        --quasar_refresh_time=120 --quasar_extra_propagations=12\
        &> benchmark/filterupdates_push_vs_pull/quasar_extraprop_push_g.json

time env/bin/python benchmark/filterupdates.py --swarm_size=400\
        --test_timedelta=2.0 --test_count=300 --quasar_size=512\
        --quasar_pull_filters=true\
        --quasar_depth=2 --quasar_ttl=64 --quasar_freshness=126\
        --quasar_refresh_time=120 --quasar_extra_propagations=14\
        &> benchmark/filterupdates_push_vs_pull/quasar_extraprop_pull_h.json

time env/bin/python benchmark/filterupdates.py --swarm_size=400\
        --test_timedelta=2.0 --test_count=300 --quasar_size=512\
        --quasar_pull_filters=false\
        --quasar_depth=2 --quasar_ttl=64 --quasar_freshness=126\
        --quasar_refresh_time=120 --quasar_extra_propagations=14\
        &> benchmark/filterupdates_push_vs_pull/quasar_extraprop_push_h.json

time env/bin/python benchmark/filterupdates.py --swarm_size=400\
        --test_timedelta=2.0 --test_count=300 --quasar_size=512\
        --quasar_pull_filters=true\
        --quasar_depth=2 --quasar_ttl=64 --quasar_freshness=126\
        --quasar_refresh_time=120 --quasar_extra_propagations=16\
        &> benchmark/filterupdates_push_vs_pull/quasar_extraprop_pull_i.json

time env/bin/python benchmark/filterupdates.py --swarm_size=400\
        --test_timedelta=2.0 --test_count=300 --quasar_size=512\
        --quasar_pull_filters=false\
        --quasar_depth=2 --quasar_ttl=64 --quasar_freshness=126\
        --quasar_refresh_time=120 --quasar_extra_propagations=16\
        &> benchmark/filterupdates_push_vs_pull/quasar_extraprop_push_i.json
